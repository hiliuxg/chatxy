

import google.generativeai as genai
import streamlit as st
import time
import random


if "history" not in st.session_state:
    st.session_state.history = []

genai.configure(api_key = st.secrets["APP_KEY"]) 
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history = st.session_state.history)


st.set_page_config(
   page_title="Chat To XYthing",
   page_icon="🔥"
)

st.title('Chat To XYthing')
st.caption('AI Chatbot That Can Talk To Anything, Powerd By Google Gemini Pro.')

with st.sidebar:
    if st.button("Start A New Chat", use_container_width = True, type="primary"):
        st.session_state.history = []
        st.rerun()
    
for message in chat.history:
    role = "assistant" if message.role == "model" else message.role
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

if prompt := st.chat_input(""):
    prompt = prompt.replace('\n', '  \n')
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown('thinking...')
        full_response = ""
        for chunk in chat.send_message(prompt, stream=True):
            word_count = 0
            random_int = random.randint(1, 10)
            for word in chunk.text:
                full_response += word
                word_count += 1
                if word_count == random_int:
                    time.sleep(0.05)
                    message_placeholder.markdown(full_response + "_")
                    word_count = 0
                    random_int = random.randint(1, 10)
        message_placeholder.markdown(full_response)
        st.session_state.history = chat.history