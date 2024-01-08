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

generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "max_output_tokens": 4096,
}
genai.configure(api_key = st.secrets["APP_KEY"]) 
model = genai.GenerativeModel('gemini-pro-vision')

st.title('上传图片问问')

with st.sidebar:
    generation_config['temperature'] = st.slider("Temperature", min_value  = 0.0, max_value = 1.0, value = 0.7, step = 0.1, label_visibility = "collapsed")
    st.caption("ℹ️ 该值越大输出越随机")


def show_message(prompt, image, loading_str):
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown(loading_str) 
        try:
            full_response = ""
            for chunk in model.generate_content([prompt, image], stream = True, safety_settings = SAFETY_SETTTINGS, generation_config = generation_config):                   
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
            st.exception(e)
       
        st.session_state.history_pic.append({"role": "assistant", "text": full_response})

if "history_pic" not in st.session_state:
    st.session_state.history_pic = []

def clear_state():
    st.session_state.history_pic = []

image = None
uploaded_file = st.file_uploader("选择一张图片...", type=["jpg", "png", "jpeg", "gif"], label_visibility='collapsed', on_change = clear_state)
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    width, height = image.size
    resized_img = image.resize((128, int(height/(width/128))), Image.LANCZOS)
    st.image(image)    

if len(st.session_state.history_pic) > 0:
    for item in st.session_state.history_pic:
        with st.chat_message(item["role"]):
            st.markdown(item["text"])

if prompt := st.chat_input("描述这张图片"):
    if image is None:
        st.warning("请您先上传图片", icon="⚠️")
    else:
        print(f"pic prompt: {prompt}")
        prompt = prompt.replace('\n', '  \n')
        with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.history_pic.append({"role": "user", "text": prompt})

        show_message(prompt, resized_img, "正在思考...")