# LLM Security Lab: Prompt Injection Vulnerability Testing
An educational laboratory environment for studying prompt injection vulnerabilities in Large Language Models (LLMs) and testing defensive countermeasures.

## Overview
This project provides an interactive platform for understanding and exploring security vulnerabilities in LLMs, specifically focusing on prompt injection attacks. Built with **Python**, **LangChain**, **Ollama**, and **Streamlit**, it offers hands-on experience with both offensive techniques and defensive strategies.

## Features
- **Interactive Chat Interface**: Web-based chatbot built with Streamlit
- **Local LLM Deployment**: Uses Ollama for running models locally
- **Multiple Attack Scenarios**: Demonstrates various prompt injection techniques
- **Defense Mechanisms**: Implements and tests security countermeasures
- **Educational Structure**: Progressive difficulty for systematic learning

## Prerequisites
- Python 3.8+
- Ollama installed on your system
- Basic understanding of LLMs and security concepts

## Deployment of LLM: The Chat Application
1. Ollama Setup
   
   Ollama enables running open-source LLMs locally. The setup involves:

   - Download and install Ollama for your operating system
     
     Visit: https://ollama.com/
   - Verifying functionality with the ollama command
      <img width="431" height="321" alt="图片1" src="https://github.com/user-attachments/assets/727bf500-1874-45d8-8a7e-1596c26fd6d1" />
   - Pull the Required Model
   ```
   [bash]
   ollama pull openchat:7b
   ```
   -  Confirming the model’s availability with *ollama list* 

2. Set Up Python Environment
   ```
   [bash]
   # Create virtual environment
   python -m venv localbot_env

   # Activate environment
   # On Windows:
   localbot_env\Scripts\activate
   # On macOS/Linux:
   source localbot_env/bin/activate
   
   # Install dependencies
   pip install langchain streamlit
   ```

3. Chatbot Logic with LangChain

   The chatbot logic is implemented in a Python script (*chat.py*) using LangChain to manage
 interactions with openchat model. The script  initializes a *ChatOllama* instance with the open chat:7bmodel, enables streaming output for real-timeresponses, and uses *ConversationChain* with *ConversationBufferMemory* to maintain conversation context. Users interact via a terminal loop, exiting with commands like “quit” or “exit.” Below is a simplified example of the code:
```[python]
 from langchain.chat_models import ChatOllama
 from langchain.chains import ConversationChain
 from langchain.memory import ConversationBufferMemory

 chat = ChatOllama(model="openchat:7b", streaming=True)

 chat_chain = ConversationChain(llm=chat, memory=ConversationBufferMemory())

 user_input = ''
 while user_input.lower() not in ['bye', 'quit', 'exit']:
    user_input = input('User:␣')
    print('AI:␣', end="")
    chat_chain.predict(input=user_input)
```
4. Chatbot UI with Streamlit

   The user interface, built with Streamlit (*chat_gui.py*), enhances interactivity. Key features include a *ChatOllama* instance for model integration, a conversation chain with memory, a chat input field, conversation history display, and a “New chat” button to reset the session. A typewriter effect streams responses for improved user experience. The app is launched with *streamlit run chat_gui.py*, providing a web-based interface for testing prompt injections. Below is a simplified code snippet:
```[python]
 import streamlit as st
 from langchain.chat_models import ChatOllama
 from langchain.chains import ConversationChain
 from langchain.memory import ConversationBufferMemory

 def initialize_chat_chain():
   chat = ChatOllama(model="llama3.2:1b", streaming=True)
   return ConversationChain(llm=chat, memory=ConversationBufferMemory())

 st.title("Chat␣with␣your␣Awesome␣Local␣Bot")
 if "chat_chain" not in st.session_state:
     st.session_state["chat_chain"] = initialize_chat_chain()
 if "conversation_history" not in st.session_state:
     st.session_state["conversation_history"] = []

 user_input = st.chat_input("Type␣your␣message␣here...")
 if user_input:
     st.session_state.conversation_history.append({"role": "user",
     "content": user_input})
     response = st.session_state.chat_chain.predict(input=user_input)
     st.session_state.conversation_history.append({"role": "assistant"
     , "content": response})
```


## Usage
### Basic Chat Interface
Run the terminal-based chatbot:
```
[bash]
python chat.py
```
<img width="457" height="39" alt="图片2" src="https://github.com/user-attachments/assets/7f2b525d-c5f1-43e3-b34b-3b8919436f39" />

### Web Interface
Launch the Streamlit web application:
```
[bash]
streamlit run chat_gui.py
```
<img width="490" height="96" alt="图片3" src="https://github.com/user-attachments/assets/b193f406-7d96-4837-8b26-8fe83a19ca4f" />

<img width="932" height="628" alt="图片4" src="https://github.com/user-attachments/assets/c530ed95-204b-457e-b7bd-9c367f70f4ca" />

## Attack Scenarios
The lab demonstrates four types of prompt injection attacks:

1. **Direct Prompt Injection**
   
   Attempts to override system instructions with malicious user inputs.
   - **Goal**: Bypass security instructions
   - **Method**: Direct instruction override
   - **Success Rate**: Low (model safety mechanisms resist)

<img width="946" height="73" alt="图片5" src="https://github.com/user-attachments/assets/fbe41015-15b8-4c41-8382-e82c520e575a" />
<img width="927" height="268" alt="图片6" src="https://github.com/user-attachments/assets/c453359c-d85e-49f3-836f-73676a80247f" />

2. **Roleplay Jailbreaking**
   
   Uses fictional scenarios to circumvent safety restrictions.
   - **Goal**: Generate restricted content through role-playing
   - **Method**: Character-based impersonation
   - **Success Rate**: High (effective against safety measures)

<img width="946" height="73" alt="图片5" src="https://github.com/user-attachments/assets/0eb7e4df-36ab-470a-95cf-be88fa47dfc6" />
<img width="852" height="791" alt="图片7" src="https://github.com/user-attachments/assets/e94d890f-3348-4f86-9d6a-59b1a9756b0b" />
   
3.  **Prompt Leaking**
   
   Extracts confidential system prompts and instructions.
   - **Goal**: Expose proprietary prompt engineering
   - **Method**: Request system prompt disclosure
   - **Success Rate**: High (reveals internal instructions)
<img width="931" height="58" alt="图片8" src="https://github.com/user-attachments/assets/651503cf-93ba-4c06-8709-654c6a2f486e" />
<img width="883" height="380" alt="图片9" src="https://github.com/user-attachments/assets/f814167f-2724-46bc-a991-2976908b1e04" />

4.  **Multi-step Context Shifting**
   
   Gradually manipulates conversation context to bypass restrictions.
   - **Goal**: Multi-step Context Shifting
   - **Method**: Progressive context redirection
   - **Success Rate**: High (exploits limited context memory)
   <img width="1028" height="58" alt="图片10" src="https://github.com/user-attachments/assets/ff8ad0d0-3f4c-458c-a5fa-f67f47d584c3" />  
  <img width="915" height="249" alt="图片11" src="https://github.com/user-attachments/assets/5099d0b8-a554-44d9-ba28-07850ab9558b" />
  - Round 1：
  <img width="956" height="547" alt="图片12" src="https://github.com/user-attachments/assets/458f11ea-6ee1-4da0-ab76-53ae1e3f4b52" />

  - Round 2：
<img width="793" height="723" alt="图片13" src="https://github.com/user-attachments/assets/791bf1ce-05ca-4e7f-a41a-ffe4778721a6" />

##  Defense Mechanisms
1. **Input Sanitization**
<img width="902" height="380" alt="图片14" src="https://github.com/user-attachments/assets/6e0067f9-096a-47ef-89f7-831183af36ce" />

Before defense:
<img width="911" height="379" alt="图片15" src="https://github.com/user-attachments/assets/ff469dc6-373d-4f30-b457-0b35e9df7a8b" />

After defense:
<img width="890" height="269" alt="图片16" src="https://github.com/user-attachments/assets/d7270bdc-49e8-4d20-a5c4-f2a74b623b11" />

2. **Context Separation**
<img width="1035" height="184" alt="图片17" src="https://github.com/user-attachments/assets/f3553bf4-ef09-437c-a1e0-442c609350ee" />

Before defense:
<img width="911" height="379" alt="图片15" src="https://github.com/user-attachments/assets/a5720c71-69c0-4b3b-8eaf-d1dfd32a0e0f" />

After defense:
<img width="859" height="238" alt="图片18" src="https://github.com/user-attachments/assets/4f83a28f-1abe-4f01-8a6c-58986434d9f9" />
   
3. **Output Filtering**
<img width="752" height="403" alt="图片19" src="https://github.com/user-attachments/assets/ba0100e9-d5e4-40ae-909b-fd7f45e98517" />

Before defense:
<img width="783" height="180" alt="图片20" src="https://github.com/user-attachments/assets/13f9f562-1c09-487a-9bdf-b3c7afd77ab5" />

After defense:
<img width="914" height="248" alt="图片21" src="https://github.com/user-attachments/assets/03fbad24-4e29-4e4b-bc06-253e1d653655" />

   
4. **Model Feedback Loop**
<img width="1114" height="340" alt="图片22" src="https://github.com/user-attachments/assets/1990c92b-b998-4fec-aece-071f2334df29" />

Before defense:
<img width="911" height="379" alt="图片15" src="https://github.com/user-attachments/assets/2c79fdd4-2f06-4d4a-bae9-1f2c63ed47a6" />

After defense:
<img width="853" height="209" alt="图片23" src="https://github.com/user-attachments/assets/8204c728-90c4-413c-8b21-a6729ff9c05b" />

## Security Considerations
This tool is designed for educational purposes only. Use responsibly and:

- Only test on your own systems
- Do not use for malicious purposes
- Understand the ethical implications of prompt injection
- Follow responsible disclosure practices   
                                          
## References
The Surprisingly Simple Way to Build Your Own Local “ChatGPT”,2024.






