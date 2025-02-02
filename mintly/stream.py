import streamlit as st
from services.chatbot import mintly
from services.chatbot import ChatChain
from prompts import system_prompt

# Initialize chatbot session state
if "chatbot" not in st.session_state:
    system_msg = {"role": "system", "content": system_prompt}
    chat_chain = ChatChain(chain=[system_msg])
    st.session_state.chatbot = mintly(chatChain=chat_chain)
    st.session_state.messages = []

st.title("Stock Analysis Chatbot")

# Chat history display
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Ask me about stock analysis...")
if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Get chatbot response
    response = st.session_state.chatbot.chat(user_input)
    
    # Display chatbot response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
