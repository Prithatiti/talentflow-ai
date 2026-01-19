# frontend/app.py

import streamlit as st
from config import PAGE_TITLE, PAGE_ICON, LAYOUT
from styles import load_css

# Import Views
from views.home import render_home
from views.generator import render_generator
from views.screener import render_screener
from views.interview import render_interview
from views.evaluate import render_evaluate

# 1. Config
st.set_page_config(page_title=PAGE_TITLE, layout=LAYOUT, page_icon=PAGE_ICON)

# 2. Load CSS (The new professional styles)
load_css()

# 3. Sidebar Navigation
with st.sidebar:
    
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.markdown("### Talentflow AI")
    
    # Using 'Home' as the first option simulates the landing page
    page = st.radio("Navigate", [
        "Home",
        "Job Description Generator", 
        "Resume Screening", 
        "AI Interviewer",
        "Evaluation Dashboard"
    ])

    st.markdown("---")
    st.caption("Powered by LLama 3.3, Gemini 2.5 & FAISS")


# 4. Page Routing
if page == "Home":
    render_home()

if page == "Job Description Generator":
    render_generator()

elif page == "Resume Screening":
    render_screener()

elif page == "AI Interviewer":
    render_interview()

elif page == "Evaluation Dashboard":
    render_evaluate()
