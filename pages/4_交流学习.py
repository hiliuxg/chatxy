
import streamlit as st

st.set_page_config(
    page_title="Chat To XYthing",
    page_icon="🔥",
    menu_items={
        'About': "# Powered by Google Gemini Pro"
    }
)


col1, col2, col3 = st.columns(3)

with col2:
    st.image("resource/wechat.jpg", caption = "欢迎加我微信，一起交流学习AI")