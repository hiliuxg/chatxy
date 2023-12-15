
from PIL import Image
import google.generativeai as genai
import streamlit as st
import time
import random

st.set_page_config(
    page_title="Chat To XYthing",
    page_icon="🔥",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)


genai.configure(api_key = st.secrets["APP_KEY"]) 
model = genai.GenerativeModel('gemini-pro-vision')


st.title('Chat To XYthing')
st.caption('Upload a image and talk to, powerd by google gemini pro vision.')


image = None
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg", "gif", "bmp"], label_visibility='hidden')
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image')

if prompt := st.chat_input(""):
    if image is None:
        st.warning("upload your image first .", icon="⚠️")
    else:
        prompt = prompt.replace('\n', '  \n')
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown('thinking...')
            full_response = ""
            for chunk in model.generate_content([prompt, image], stream=True):
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
        

