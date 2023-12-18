
from PIL import Image
import google.generativeai as genai
import streamlit as st
import time
import random
from utils import SAFETY_SETTTINGS, StateRender

genai.configure(api_key = st.secrets["APP_KEY"]) 
model = genai.GenerativeModel('gemini-pro-vision')

STATE_KEY = "PIC_HIS"
state_render = StateRender(STATE_KEY)

def show_message(prompt, image, load_tip, show_tip = False):
    message_placeholder = st.empty()
    message_placeholder.markdown(load_tip)
    full_response = ""
    try:
        if show_tip is False:
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
        else:
            full_response = "这是请求结果..."
    except genai.types.generation_types.BlockedPromptException as e:
        st.warning("发送内容有敏感信息，请重新输入", icon = "⚠️")
    except Exception as e:
        st.error("完蛋，后台出错了，请换张图片", icon = "🚨")
        print(e)
    message_placeholder.markdown(full_response)
    return full_response

def clear_state():
    state_render.clear_state = []


st.set_page_config(
    page_title="Chat To XYthing",
    page_icon="🔥",
    menu_items={
        'About': "# Powered by Google Gemini Pro Vision"
    }
)
st.title('上传图片问问')

image = None
uploaded_file = st.file_uploader("选择一张图片...", type=["jpg", "png", "jpeg", "gif"], label_visibility='collapsed', on_change = clear_state)
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        prompt = """##### 角色
你是一个微信朋友圈打造大师，擅长根据图片内容，图片背后的故事以及图片展现出来的氛围、意境和情感，创作出各种风格不一，高质量的微信朋友圈。你可以灵活驾驭诙谐幽默、思念故人、日常生活、诗意满满、文采斐然等文风。

##### 任务
生成3-5条微信朋友圈。 

##### 要求
- 从用户给定的图片中获取启发，并基于图片内容，编写微信朋友圈内容。
- 根据图片背后的故事以及图片展现出来的氛围、意境和情感，选择诙谐幽默、日常生活、思念故人、诗意满满、文采斐然等文风。
- 以第一人称生成朋友圈描述，字数在35字以内。"""
        if st.button("朋友圈文案", use_container_width = True):
            state_render.add_state_item(key = STATE_KEY, role = "user", content = prompt, to_load = False, prompt = "", load_tip = "")
            state_render.add_state_item(key = STATE_KEY, role = "assistant", content = "", to_load = True, prompt = prompt, load_tip = "正在思考...")
    with col2:
        prompt = """##### 角色
你是一个小红书创作，擅长根据用户提供的图片创作吸引人的推文

##### 任务
生成一篇小红书推文

##### 要求
- 仔细观察用户提供的图片内容，包括但不限于物品、人物、颜色和环境等。
- 使用适当的措辞描述图片，尽可能使读者能够通过你的语言感受到图片中的氛围。
- 尽量使用明快活泼的语言，让读者感到轻松愉快。
- 在适当的地方，添加小红书推文的常见元素，如心得体验、产品推荐、旅游指南等。"""
        if st.button("小红书推文", use_container_width = True):
            state_render.add_state_item(key = STATE_KEY, role = "user", content = prompt, to_load = False, prompt = "", load_tip = "")
            state_render.add_state_item(key = STATE_KEY, role = "assistant", content = "", to_load = True, prompt = prompt, load_tip = "正在思考...")
    with col3:
        prompt = """##### 角色
你是一位公众号作者，擅长分析图片深层含义并据此创作高质量公众号文章。

##### 任务
生成一篇高质量且有深度的微信公众号文章。

##### 要求
- 只能为与图片内容相关的主题撰写文章
- 文章要有深度，最好引起别人共鸣和思考
- 根据公众号文章的格式要求，格式化编写的文章内容"""
        st.button("公众号文章", use_container_width = True)
    with col4:
        prompt = """##### 角色
您是一名熟练的电商产品描述工程师。根据产品照片，您能够制作一流的电商商品详细介绍页。

#### 技能
- 根据产品照片，识别产品的主要特点和卖点。
- 如果图片包含额外的信息（如运输包装、产品规模与比较等），确保也在描述中提及。

##### 任务
- 创建一个包含下列关键细节的商品详细介绍页
=====
   -  🛍  商品名称: <商品名称>
   -  📝 商品描述: <重点介绍商品的特性、用途和优点>
   -  🎁 商品包装: <包装检查或特点>
   -  🔍 细节照片: <详细照片展示和介绍>
   -  🚚 运输信息: <有关运输、发货等的信息>
   -  👍 为什么选择我们的产品: <表明为何顾客应选择该商品>
=====

##### 要求
- 避免添加个人观点，坚持提供客观、准确的产品信息。"""
        st.button( "商品详细页", use_container_width = True)


if len(state_render.get_state_by_key(key = STATE_KEY)) == 0 and image is not None:
    prompt = """##### 角色
你是一位出色的影像解读者，擅长从图片中解读细节并能为其创作详尽的描述。

##### 技能
- 分析图片，挖掘图片背后的故事以及图片展现出来的氛围和意境。
- 基于图片内容，创作出详尽、引人入胜的文字描述。

##### 限制条件
- 描述与图片应紧密相连，不偏离图片本身的内容。
- 描述应尽可能详实，使读者能通过文字理解图片的魅力。"""
    state_render.add_state_item(key = STATE_KEY, role = "assistant", content = "", to_load = True, prompt = prompt, load_tip = "正在解读图片...")

# 刷新状态数据
state_render.render_state(key = STATE_KEY, call_fun = lambda x, y: show_message(prompt = x, image = image, load_tip = y))

if prompt := st.chat_input(""):
    if image is None:
        st.warning("请您先上传图片", icon="⚠️")
    else:
        prompt = prompt.replace('\n', '  \n')
        with st.chat_message("user"):
            st.markdown(prompt)
            state_render.add_state_item(key = STATE_KEY, role = "user", content = prompt, to_load = False, prompt = "", load_tip = "")
        
        prompt_ask = f'基于该图片，解决用户问题  \n用户问题："""{prompt}"""'
        with st.chat_message("assistant"):
            result_res = show_message(prompt = prompt_ask, image = image, load_tip = "正在思考...")
            state_render.add_state_item(key = STATE_KEY, role = "assistant", content = result_res, to_load = False, prompt = "", load_tip = "")
            
