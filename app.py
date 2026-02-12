import streamlit as st
from openai import OpenAI
from gtts import gTTS
import io
from PIL import Image
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection # The "Bridge" to Google Sheets

# 1. STYLE & PAGE SETUP (Always first)
st.set_page_config(page_title="Oga Tutor", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: white; }
    .stSidebar { background-color: #008751; }
    h2 { color: #008751; font-size: 28px !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("## 🇳🇬 Oga Tutor: Study & Save")

# 2. CONNECTIONS (OpenAI and Google Sheets)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
# This connects to the spreadsheet link you will put in your Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. SIDEBAR (The Profile Section)
with st.sidebar:
    st.write("### 👤 Student Profile")
    student_name = st.text_input("Your Name:", placeholder="e.g. Tunde")
    if student_name:
        st.success(f"Welcome, {student_name}!")

# 4. CHAT HISTORY SETUP
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a professional teacher. Answer 90% in formal English and 10% in Pidgin at the end."}
    ]

# 5. SCANNER SECTION
st.write("📸 **Scan textbook question:**")
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

# 6. DISPLAY OLD MESSAGES
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 7. THE BRAIN & SAVING LOGIC
if prompt := st.chat_input("Ask Oga Tutor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Get answer from AI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        answer = response.choices[0].message.content
        st.markdown(answer)
        
        # --- SAVE TO GOOGLE SHEETS ---
        if student_name:
            new_entry = pd.DataFrame([{
                "Name": student_name,
                "Question": prompt,
                "Answer": answer,
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }])
            # This "appends" the new lesson to your spreadsheet
            existing_data = conn.read()
            updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
            conn.update(data=updated_df)
        
        # Voice & Share buttons
        tts = gTTS(text=answer, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp)
        
        st.session_state.messages.append({"role": "assistant", "content": answer})
