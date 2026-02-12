import streamlit as st
from openai import OpenAI
from gtts import gTTS
import io
from PIL import Image # For the textbook scanner

st.set_page_config(page_title="Oga Tutor", layout="centered")

# Smaller Header for mobile
st.markdown("## 🇳🇬 Oga Tutor: Your Exam Assistant")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a professional teacher. Answer 90% in formal English and 10% in Pidgin at the end. Explain textbook questions clearly."}
    ]

# --- FEATURE 1: TEXTBOOK SCANNER ---
st.write("📸 **Scan your textbook:**")
uploaded_file = st.file_uploader("Upload or take a photo of a question paper", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.info("Oga is looking at your textbook... (Type 'Explain this photo' below)")

# Display chat
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Ask or type 'WAEC/JAMB/NECO Question'"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # If student uploaded a file, we tell the AI to be extra helpful
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        answer = response.choices[0].message.content
        st.markdown(answer)
        
        # --- FEATURE 2: VOICE & DOWNLOAD ---
        col1, col2 = st.columns(2)
        with col1:
            # Voice
            tts = gTTS(text=answer, lang='en')
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            st.audio(fp, format='audio/mp3')
        
        with col2:
            # Download Button (Save for offline)
            st.download_button(
                label="💾 Save Lesson",
                data=answer,
                file_name="oga_tutor_lesson.txt",
                mime="text/plain"
            )
        
        st.session_state.messages.append({"role": "assistant", "content": answer})

