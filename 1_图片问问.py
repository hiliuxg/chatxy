
from PIL import Image
import google.generativeai as genai
import streamlit as st
import time
import random
from utils import SAFETY_SETTTINGS

st.set_page_config(
    page_title="Chat To XYthing",
    page_icon="🔥",
    menu_items={
        'About': "# Powered by Google Gemini Pro Vision"
    }
)

genai.configure(api_key = st.secrets["APP_KEY"]) 
model = genai.GenerativeModel('gemini-pro-vision')

st.title('上传图片问问')


def show_message(prompt, image, loading_str):
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown(loading_str)
        full_response = ""
        try:
            print(f"prompt:{prompt}")
            for chunk in model.generate_content([prompt, image], stream = True, safety_settings = SAFETY_SETTTINGS):                   
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
        except genai.types.generation_types.BlockedPromptException as e:
            st.warning("发送内容有敏感信息，请重新输入", icon = "⚠️")
        except Exception as e:
            st.error("完蛋，后台出错了，请换张图片", icon = "🚨")
            print(e)
        message_placeholder.markdown(full_response)
        st.session_state.history_pic.append({"role": "assistant", "text": full_response})

if "history_pic" not in st.session_state:
    st.session_state.history_pic = []

def clear_state():
    st.session_state.history_pic = []

image = None
uploaded_file = st.file_uploader("选择一张图片...", type=["jpg", "png", "jpeg", "gif", "bmp"], label_visibility='collapsed', on_change = clear_state)
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image)    

if len(st.session_state.history_pic) == 0 and image is not None:
    show_message("详细的描述该图片内容，并说明该图片展现出来的氛围或意境", image, "正在解读图片内容...")
    tips = """接下来，您可以尝试输入以下问题
* 基于该图片的氛围或者意境，以第一人称，帮忙我生成1条微信朋友圈文案
* 根据这张图片写一篇简短的小红书推文，它应该包括对照片内容的描述，吸引人点击"""
    #with st.chat_message("assistant"):
    #    st.markdown(tips)
    #    st.session_state.history_pic.append({"role": "assistant", "text": tips})
    
else:
    for item in st.session_state.history_pic:
        with st.chat_message(item["role"]):
            st.markdown(item["text"])

if prompt := st.chat_input(""):
    if image is None:
        st.warning("请您先上传图片", icon="⚠️")
    else:
        prompt = prompt.replace('\n', '  \n')
        with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.history_pic.append({"role": "user", "text": prompt})
           
        prompt_plus = f'基于该图片，解决用户问题  \n用户问题："""{prompt}"""'
        show_message(prompt_plus, image, "正在思考...")
        

