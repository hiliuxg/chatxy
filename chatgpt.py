from openai import OpenAI
import streamlit as st


st.set_page_config(
   page_title="Chat To XYthing",
   page_icon="🔥"
)

client = OpenAI(
    api_key = st.secrets["APP_KEY"]
)

st.title('Chat To XYthing')
st.caption('使用ChatGPT3.5提供服务，您可以向我提问任何问题~')

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input(""):
    prompt = prompt.replace('\n', '  \n')
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown('正在思考...')
        full_response = ""
        for response in client.chat.completions.create(
            model = st.session_state["openai_model"],
            messages = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages[-5:]
            ],
            stream=True
        ):
            res_tmp = response.choices[0].delta.content
            full_response += res_tmp if res_tmp is not None else ''
            message_placeholder.markdown(full_response + "_")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})