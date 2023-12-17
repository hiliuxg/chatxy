

import google.generativeai as genai
import streamlit as st
import time
import random
from utils import SAFETY_SETTTINGS


genai.configure(api_key = st.secrets["APP_KEY"]) 
model = genai.GenerativeModel('gemini-pro')


if "history_ze" not in st.session_state:
    st.session_state.history_ze = []


st.set_page_config(
    page_title="Chat To XYthing",
    page_icon="🔥",
    menu_items={
        'About': "# Powered by Google Gemini Pro"
    }
)

st.title("中英互译助手")
st.caption("输入您需要翻译的语句，我将完成翻译~")


with st.sidebar:
    if st.button("清空聊天区域", use_container_width = True, type="primary"):
        st.session_state.history_ze = []
        st.rerun()

# show history_pic
for item in st.session_state.history_ze:
    with st.chat_message(item["role"]):
        st.markdown(item["text"])

if prompt := st.chat_input(""):
    prompt = prompt.replace('\n', '  \n')
    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.history_ze.append({"role": "user", "text": prompt})
    
    prompt_plus = f'''"""# 角色
你是一位优秀的中英互译专家
## 技能

### 技能1：进行中英翻译
- 理解用户提供的含义，并进行准确的中英翻译
- 注意文化差异，并在翻译过程中给予适当的指导
- 尽量保持原始信息的准确性和完整性 

### 技能2：进行英中翻译
- 理解源语言的文本内容，准确无误地将其翻译成目标语言
- 注重保持各种形式的对等性
- 注重考虑到词汇、语法等层面的差异性 

## 限制
- 在执行翻译任务时，始终保持尊重并遵守原文内容
- 不引入无关的个人观点，确保翻译准确无误
- 在情绪表达上，尽量保持原始文本的风格和语境
- 只输出翻译的结果，不要写解释和其他任何内容

如果明白，请翻译下面这句话：“{prompt}”"""'''
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("正在思考...")
        full_response = ""
        try:
            print(f"prompt:{prompt_plus}")
            for chunk in model.generate_content(prompt_plus, stream = True, safety_settings = SAFETY_SETTTINGS):                   
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

        st.session_state.history_ze.append({"role": "assistant", "text": full_response})
