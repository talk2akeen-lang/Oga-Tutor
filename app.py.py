import streamlit as st
from openai import OpenAI

# 1. Setup Page - Mobile Friendly
st.set_page_config(page_title="Oga Tutor JAMB Prep", page_icon="🎓")
st.markdown("""<style> .main { background-color: #f5f7f9; } </style>""", unsafe_allow_html=True)

st.title("🎓 Oga Tutor")
st.caption("Your personal JAMB & WAEC assistant")

# 2. Enter API Key (Keep this secure!)
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

if api_key:
    client = OpenAI(api_key=api_key)

    # 3. Initialize Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are 'Oga Tutor', a witty Nigerian academic mentor. Explain topics using local analogies (Danfo, Jollof, Market logic). Mix standard English with light Pidgin. Focus on JAMB/WAEC syllabus."}
        ]

    # Display Chat
    for message in st.session_state.messages[1:]: # Skip system prompt
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 4. Chat Input
    if prompt := st.chat_input("Ask me any subject (e.g., Physics, Govt)..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
else:
    st.info("Please enter your OpenAI API Key in the sidebar to start learning!")