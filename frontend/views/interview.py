# frontend/views/interview.py

import streamlit as st
import requests
from config import API_URL

def render_interview():
    st.title("🤖 AI Preliminary Interview")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Context Input
    context = st.text_area("1. Paste Job Description Here:", height=100, key="interview_context", placeholder="Paste the JD here to give the AI context...")
    
    # START BUTTON LOGIC
    if len(st.session_state.messages) == 0:
        if st.button("Start Interview"):
            if not context:
                st.error("Please paste a Job Description first.")
            else:
                with st.spinner("AI is preparing the first question..."):
                    try:
                        res = requests.post(f"{API_URL}/interview_bot", json={
                            "history": "", 
                            "message": "START_INTERVIEW", # Hidden trigger
                            "context": context
                        })
                        
                        if res.status_code == 200:
                            bot_reply = res.json().get("reply")
                            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                            st.rerun()
                        else:
                            st.error("Error: Could not start interview.")
                    except Exception as e:
                        st.error(f"Connection Error: {e}")

    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if len(st.session_state.messages) > 0:
        if prompt := st.chat_input("Type your answer here..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.spinner("Interviewer is thinking..."):
                history_str = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                try:
                    res = requests.post(f"{API_URL}/interview_bot", json={
                        "history": history_str, 
                        "message": prompt,
                        "context": context
                    })
                    bot_reply = res.json().get("reply")
                    
                    with st.chat_message("assistant"):
                        st.markdown(bot_reply)
                    
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                except Exception as e:
                    st.error(f"Error: {e}")
