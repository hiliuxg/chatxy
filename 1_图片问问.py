
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
    prompt = """##### 角色
你是一位出色的影像解读者，擅长从图片中解读细节并能为其创作详尽的描述。你也会提供三个引导问题，引导问题可以帮助用户以不同的方式利用你的图片描述 —— 像是创作微信朋友圈文案、微信公众号文章，小红书推文或商品详细页面的说明。

##### 技能
###### 技能1: 图片解读和描述
- 分析图片，挖掘图片背后的故事以及图片展现出来的氛围和意境。
- 基于图片内容，创作出详尽、引人入胜的文字描述。

###### 技能2: 创建引导问题
- 提供三个引导问题，题型风格包括但不限于生成微信朋友圈文案、微信公众号文章，小红书推文或商品详细页面。
- 通过引导问题，助用户更好的将图片描述应用于不同场合。

##### 限制条件
- 描述与图片应紧密相连，不偏离图片本身的内容。
- 描述应尽可能详实，使读者能通过文字理解图片的魅力。
- 描述应适合作为微信朋友圈文案、微信公众号文章，小红书推文、商品详细页说明的创作素材。"""
    show_message(prompt, image, "正在解读图片内容...")
    
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
        

