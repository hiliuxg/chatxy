

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


generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "max_output_tokens": 4096,
}
genai.configure(api_key = st.secrets["APP_KEY"]) 
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history = st.session_state.history)

st.title("Chat To XYthing")
st.caption("我是您的AI助手，您可以要求我做任何事情~")

with st.sidebar:
    if st.button("清空聊天区域", use_container_width = True, type="primary"):
        st.session_state.history = []
        st.rerun()

    st.divider()
    generation_config['temperature'] = st.slider("Temperature", min_value  = 0.0, max_value = 1.0, value = 0.7, step = 0.1, label_visibility = "collapsed")
    st.caption("ℹ️ 该值越大输出越随机")
    
for message in chat.history:
    role = "assistant" if message.role == "model" else message.role
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

if prompt := st.chat_input(""):
    print(f"xy prompt: {prompt}")
    prompt = prompt.replace('\n', '  \n')
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("正在思考...")
        try:
            full_response = ""
            for chunk in chat.send_message(prompt, stream=True, safety_settings = SAFETY_SETTTINGS, generation_config = generation_config): 
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
            print(e)
            st.warning("发送内容有敏感信息，请重新输入", icon = "⚠️")
        except Exception as e:
            print(e)
            st.error("完蛋，后台出错了，请重新输入", icon = "🚨")
        st.session_state.history = chat.history