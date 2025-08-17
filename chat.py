

from langchain.chat_models import ChatOllama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
 
# Ollama should be up and running on your local system
chat = ChatOllama(
    model="llama3.2:1b",  # change the model as per your requirements
    streaming=True,
    callback_manager=CallbackManager(
        [StreamingStdOutCallbackHandler()]
    ),
    verbose=False,
    temperature=0.8  # Tweak the value to find what works best for your requirements
)
 
chat_chain = ConversationChain(
    llm=chat,
    memory=ConversationBufferMemory(), # change the memory type as per your requirements
)
 
user_input = ''
quit_signal = ['bye', 'quit', 'exit', 'break', 'stop']
while user_input.lower() not in quit_signal:
    user_input = input('User: ')
    print(f'\nYou: {user_input}')
    print('AI: ', end="")
    chat_chain.predict(input=user_input)
