# frontend/views/home.py

import streamlit as st

def render_home():
    # --- HERO SECTION ---
    st.markdown("""
        <div class="hero-container">
            <div style="margin-bottom: 1rem;">
                <span style="background: rgba(45, 212, 191, 0.1); color: #2dd4bf; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 600;">
                    ✨ AI-Powered Recruiting Platform
                </span>
            </div>
            <h1 class="hero-title">
                Hire Smarter with <br>
                <span class="highlight">TalentflowAI</span>
            </h1>
            <p class="hero-subtitle">
                Accelerate your hiring cycle with AI that screens resumes, 
                generates job descriptions, and conducts preliminary interviews.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # --- FEATURES GRID ---
    # We use st.columns to create the grid layout
    
    st.markdown("### Platform Modules")
    
    # Row 1
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <div class="card-icon">📄</div>
                <div class="card-title">Smart Resume Screening</div>
                <p class="card-text">
                    AI automatically scores and ranks resumes against job requirements, 
                    highlighting the best matches instantly using FAISS Vector Search.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="feature-card">
                <div class="card-icon">📝</div>
                <div class="card-title">JD Generator</div>
                <p class="card-text">
                    Generate professional, inclusive job descriptions in seconds 
                    with Large Language Models that understand your company's voice.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="feature-card">
                <div class="card-icon">🤖</div>
                <div class="card-title">AI Interviews</div>
                <p class="card-text">
                    Conduct preliminary screening interviews with an AI agent 
                    that evaluates responses and provides detailed transcripts.
                </p>
            </div>
        """, unsafe_allow_html=True)

    # Row 2 (Mapping your "Evaluation Dashboard" to the "Analytics" card)
    st.markdown("<br>", unsafe_allow_html=True) # Spacer
    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown("""
            <div class="feature-card">
                <div class="card-icon">📊</div>
                <div class="card-title">Analytics Dashboard</div>
                <p class="card-text">
                    Track hiring metrics and audit AI performance with 
                    comprehensive "LLM-as-a-Judge" evaluation reports.
                </p>
            </div>
        """, unsafe_allow_html=True)