import streamlit as st
from openai import OpenAI

# 1. Nigerian Green-White-Green Design
st.set_page_config(page_title="Oga Tutor", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: white; }
    .stSidebar { background-color: #008751; }
    h1, h2, h3 { color: #008751; }
    </style>
    """, unsafe_allow_html=True)

st.title("🇳🇬 Oga Tutor: Your JAMB/WAEC/NECO Assistant")

# 2. Secret Key Connection (No more asking for key in sidebar!)
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    st.error("Oga, your API Key is missing in Streamlit Secrets!")

# 3. The Language Instruction (90% English, 10% Pidgin)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Oga Tutor, a helpful teacher for WAEC/NECO and JAMB. Speak 90% formal English, but use 10% Pidgin for emphasis or to explain difficult parts. Be very clear."}
    ]

# Display chat history
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Ask your WAEC/NECO/JAMB question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # or gpt-4o
            messages=st.session_state.messages
        )
        answer = response.choices[0].message.content
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
