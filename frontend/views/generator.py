# frontend/views/generator.py

import streamlit as st
import requests
from config import API_URL

def render_generator():
    st.title("📝 Intelligent JD Generator")
    st.markdown("Generate professional Job Descriptions in seconds using LLMs.")
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            role = st.text_input("Job Role", "Senior Python Developer")
            exp = st.number_input("Years of Experience", 1, 20, 5)
        with col2:
            skills = st.text_input("Required Skills", "Python, FastAPI, AWS, Docker")
        
        if st.button("Generate JD"):
            with st.spinner("Consulting AI..."):
                try:
                    res = requests.post(f"{API_URL}/generate_jd", json={"role": role, "skills": skills, "experience": str(exp)})
                    if res.status_code == 200:
                        jd_data = res.json().get("jd")
                        st.session_state['generated_jd'] = jd_data
                        st.success("JD Generated!")
                    else:
                        st.error("Error connecting to backend.")
                except Exception as e:
                    st.error(f"Connection Failed: {e}")

    if 'generated_jd' in st.session_state:
        st.markdown("### Preview")
        st.text_area("Copy your JD:", st.session_state['generated_jd'], height=400)
