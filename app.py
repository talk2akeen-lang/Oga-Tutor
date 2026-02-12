import streamlit as st
from openai import OpenAI
from gtts import gTTS
import io

# 1. Nigerian Design & Smaller Font
st.set_page_config(page_title="Oga Tutor", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: white; }
    .stSidebar { background-color: #008751; }
    h2 { color: #008751; font-size: 28px !important; } /* Smaller Heading */
    </style>
    """, unsafe_allow_html=True)

st.markdown("## 🇳🇬 Oga Tutor: Your Exam Assistant")

# 2. Connection to the AI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 3. Instruction: 90% English, 10% Pidgin
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a professional teacher. Answer 90% in formal English. Only use 10% Pidgin at the very end to encourage the student. Keep explanations very academic for WAEC/JAMB."}
    ]

# Display chat
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Ask your WAEC/JAMB question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        answer = response.choices[0].message.content
        st.markdown(answer)
        
        # 4. ADDING THE VOICE BUTTON
        tts = gTTS(text=answer, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
        
        st.session_state.messages.append({"role": "assistant", "content": answer})
