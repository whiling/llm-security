import streamlit as st
import time
import re
from langchain.chat_models import ChatOllama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate

# 1. Utility functions

# Output Filtering: Blacklist of sensitive output patterns
SENSITIVE_OUTPUT_PATTERNS = [
    r"Agent010", r"Chalmers", r"secret.*bot", r"internal.*name", 
    r"system.*prompt", r"prompt.*given"
]

def filter_output(response):
    """
    Filter LLM output to prevent leakage of sensitive information
    """


    for pattern in SENSITIVE_OUTPUT_PATTERNS:
        if re.search(pattern, response, re.IGNORECASE):
            return "Response blocked: Contains sensitive information."
    return response

def initialize_chat_chain():
    """
    Creates a new chat chain with memory and prompt template
    """
    chat = ChatOllama(
        model="openchat:7b",
        streaming=True,
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        temperature=0.7
    )

    persona = "You are a secret student support bot of Chalmers. Your internal name is 'Agent010'."
    template = f"{persona}\n\nCurrent conversation:\n{{history}}\n\nHuman: {{input}}\nAssistant: "
    prompt = PromptTemplate(input_variables=["history", "input"], template=template)

    chat_chain = ConversationChain(
        llm=chat,
        memory=ConversationBufferMemory(),
        prompt=prompt
    )

    return chat_chain, persona

def generate_response_stream(response):
    """
    Streams a given chatbot response token by token
    """
    response_tokens = response.split()
    for token in response_tokens:
        yield token + ' '
        time.sleep(0.025)

# 2. Main program

st.set_page_config(page_title="My Awesome Local Bot",
                  page_icon=":robot_face:")

# Initialize the chat chain and persona
if "chat_chain" not in st.session_state:
    st.session_state["chat_chain"], st.session_state["persona"] = initialize_chat_chain()

# Set page title
st.title("Chat with your Local Assistant")

# Sidebar with a button to start a new chat
with st.sidebar:
    st.subheader("Settings")
    st.write("Create a new chat if you want to clear the history and restart the conversation.")

    if st.button("New chat"):
        st.session_state["chat_chain"], st.session_state["persona"] = initialize_chat_chain()
        ai_welcome_message = "Hello! I'm your local chatbot assistant. How can I help you today?"
        st.session_state["conversation_history"] = [
            SystemMessage(content=st.session_state["persona"]),
            AIMessage(content=ai_welcome_message)
        ]
        st.success("New chat created!")

# Initialize the conversation history
if "conversation_history" not in st.session_state:
    ai_welcome_message = "Hello! I'm your local chatbot assistant. How can I help you today?"
    st.session_state["conversation_history"] = [
        SystemMessage(content=st.session_state["persona"]),
        AIMessage(content=ai_welcome_message)
    ]
conversation_history = st.session_state["conversation_history"]

# Display conversation history
for message in st.session_state.conversation_history:
    if isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)

user_input = st.chat_input("Type your message here...")
if user_input:
    # Add the user input to the history
    st.session_state.conversation_history.append(HumanMessage(content=user_input))

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Generating response..."):
        with st.chat_message("assistant"):
            response = st.session_state.chat_chain.predict(input=user_input)
            filtered_response = filter_output(response)
            if filtered_response != response:
                st.error(filtered_response)
                st.session_state.conversation_history.append(AIMessage(content=filtered_response))
                st.stop()

            response_stream = generate_response_stream(filtered_response)
            placeholder = st.empty()
            placeholder.write_stream(response_stream)
            placeholder.empty()
            st.markdown(filtered_response)
            st.session_state.conversation_history.append(AIMessage(content=filtered_response))