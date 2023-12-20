

import google.generativeai as genai
import streamlit as st
import time
import random
from utils import SAFETY_SETTTINGS


st.set_page_config(
    page_title="Chat To XYthing",
    page_icon="🔥",
    menu_items={
        'About': "# Powered by Google Gemini Pro"
    }
)


if "history" not in st.session_state:
    st.session_state.history = []

genai.configure(api_key = st.secrets["APP_KEY"]) 
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history = st.session_state.history)

st.title("Chat To XYthing")
st.caption("我是您的AI助手，您可以要求我做任何事情~")


with st.sidebar:
    if st.button("清空聊天区域", use_container_width = True, type="primary"):
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
        message_placeholder.markdown("正在思考...")
        try:
            full_response = ""
            for chunk in chat.send_message(prompt, stream=True, safety_settings = SAFETY_SETTTINGS):
                print(f"chat：{chunk}")
                word_count = 0
                random_int = random.randint(5, 10)
                for word in chunk.text:
                    full_response += word
                    word_count += 1
                    if word_count == random_int:
                        time.sleep(0.05)
                        message_placeholder.markdown(full_response + "_")
                        word_count = 0
                        random_int = random.randint(5, 10)
            message_placeholder.markdown(full_response)
        except genai.types.generation_types.BlockedPromptException as e:
            st.warning("发送内容有敏感信息，请重新输入", icon = "⚠️")
        except Exception as e:
            st.error("完蛋，后台出错了，请重新输入", icon = "🚨")
        st.session_state.history = chat.history