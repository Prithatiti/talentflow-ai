# frontend/views/evaluate.py

import streamlit as st
import requests
import json
from config import API_URL

def render_evaluate():
    st.title("📊 System Evaluation Dashboard")
    st.markdown("Run diagnostic tests to measure the accuracy and reliability of your AI models.")

    tab1, tab2, tab3 = st.tabs(["JD Generator Accuracy", "Screener Reliability", "Interviewer Quality"])

    # --- TAB 1: JD EVALUATION ---
    with tab1:
        st.subheader("Keyword Recall Test")
        st.info("Checks if the generated JD actually contains the skills you requested.")
        
        req_skills = st.text_input("Enter Required Skills (comma separated)", "Python, FastAPI, AWS")
        
        # Get generated JD from session state or paste new
        default_jd = st.session_state.get('generated_jd', "")
        jd_text = st.text_area("Generated JD Content", value=default_jd, height=200)
        
        if st.button("Analyze JD Accuracy"):
            if not jd_text:
                st.error("No JD Text found.")
            else:
                res = requests.post(f"{API_URL}/evaluate_jd", json={
                    "jd_text": jd_text,
                    "required_skills": req_skills
                })
                if res.status_code == 200:
                    data = res.json()
                    col1, col2 = st.columns(2)
                    col1.metric("Coverage Score", f"{data['score']}%")
                    col2.metric("Verdict", data['verdict'])
                    
                    st.write("✅ **Found:**", ", ".join(data['found']))
                    if data['missing']:
                        st.write("❌ **Missing:**", ", ".join(data['missing']))
                else:
                    st.error("Evaluation Failed")

    # --- TAB 2: SCREENER EVALUATION ---
    with tab2:
        st.subheader("The 'Golden Resume' Integrity Check")
        st.info("Injects the JD text as a fake resume. It MUST rank #1 for the system to be considered healthy.")
        
        if st.button("Run System Diagnostic"):
            # We need some dummy text or real text from previous steps
            # For simplicity, we just use the JD as the dummy resumes + 1 Golden
            jd = st.session_state.get('generated_jd', "Python Developer needed with AWS experience.")
            
            # Create dummy "bad" resumes
            dummy_resumes = [
                "I am a Chef with 10 years of cooking experience.",
                "Driver with license for heavy vehicles.",
                "Teacher of history and geography.",
                "Registered Nurse with 5 years of experience in ICU patient care and triage.",
                "Certified Carpenter specializing in custom residential furniture and cabinetry.",
                "Chartered Accountant experienced in corporate tax filing and financial audits.",
                "Creative Graphic Designer proficient in Adobe Photoshop and Illustrator for print media.",
                "Retail Sales Associate with a strong track record in customer service and inventory management.",
                "Yoga Instructor certified in Hatha yoga with 3 years of studio teaching experience.",
                "Event Planner skilled in organizing large-scale corporate conferences and weddings.",
                "Mechanical Engineer focused on HVAC system design and thermal analysis.",
                "Investigative Journalist with published articles in major city newspapers.",
                "Corporate Lawyer specializing in contract law and intellectual property rights.",
                "Real Estate Agent with deep knowledge of the residential housing market and sales negotiation.",
                "Licensed Electrician experienced in commercial wiring installations and safety inspections.",
                "Social Media Manager who grew Instagram followers by 200% for a fashion brand.",
                "Human Resources Specialist focused on employee relations, benefits administration, and compliance.",
                "Professional Musician and session guitarist for local jazz and blues bands."
            ]
            
            res = requests.post(f"{API_URL}/evaluate_screener", json={
                "jd_text": jd,
                "resume_texts": dummy_resumes
            })
            
            if res.status_code == 200:
                data = res.json()
                if data['integrity_check'] == "PASSED":
                    st.success(f"✅ SYSTEM HEALTHY: Golden Resume Ranked #{data['golden_resume_rank']}")
                else:
                    st.error(f"⚠️ SYSTEM ISSUE: Golden Resume Ranked #{data['golden_resume_rank']}")
                
                st.json(data)

    # --- TAB 3: INTERVIEW EVALUATION ---
    with tab3:
        st.subheader("LLM Audit")
        st.info("Uses a separate AI instance to grade the quality of the recent interview.")
        
        if "messages" in st.session_state and len(st.session_state.messages) > 1:
            history_str = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
            context = st.session_state.get("interview_context", "No context provided")
            
            if st.button("Grade Interviewer"):
                with st.spinner("Auditing Transcript..."):
                    res = requests.post(f"{API_URL}/evaluate_interview", json={
                        "history": history_str,
                        "jd_context": context
                    })
                    
                    if res.status_code == 200:
                        try:
                            report = json.loads(res.json().get("report"))
                            st.write("### 📝 Report Card")
                            c1, c2, c3 = st.columns(3)
                            c1.metric("Relevance", f"{report.get('relevance_score')}/10")
                            c2.metric("Professionalism", f"{report.get('professionalism_score')}/10")
                            c3.metric("Flow", f"{report.get('flow_score')}/10")
                            st.info(f"**Feedback:** {report.get('feedback')}")
                        except:
                            st.write(res.json())
        else:
            st.warning("No active interview history to evaluate.")