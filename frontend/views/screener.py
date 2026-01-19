# frontend/views/screener.py

import streamlit as st
import requests
import pandas as pd
from config import API_URL

def render_screener():
    st.header("🏆 Resume Ranking Board")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.info("Upload multiple resumes to see who comes out on top!")
    with col2:
        # Fun metric
        if 'last_ranking_count' in st.session_state:
            st.metric("Candidates Ranked", st.session_state['last_ranking_count'])

    # Input Section
    jd_input = st.text_area("1. Paste Job Description", 
                           value=st.session_state.get('generated_jd', ""), 
                           height=150,
                           placeholder="Paste JD here...")
    
    uploaded_files = st.file_uploader("2. Upload CVs (Max 10 recommended)", 
                                     type=["pdf"], 
                                     accept_multiple_files=True)
    
    if st.button("Analyze Candidates", type="primary"):
        if not uploaded_files or not jd_input:
            st.warning("Please provide both a JD and at least one Resume.")
            return

        with st.spinner("Analyzing skills & calculating scores..."):
            files = [('files', (f.name, f, 'application/pdf')) for f in uploaded_files]
            try:
                res = requests.post(f"{API_URL}/screen_resumes", data={"jd_text": jd_input}, files=files)
                
                if res.status_code == 200:
                    results = res.json().get("results")
                    if not results:
                        st.error("No readable text found in documents.")
                        return
                    
                    # Store count for metric
                    st.session_state['last_ranking_count'] = len(results)
                    
                    # Convert to DataFrame
                    df = pd.DataFrame(results)
                    
                    # --- NEW: Generate General Remarks based on Score ---
                    def get_remark(score):
                        if score >= 45: return "🌟 Highly Recommended"
                        elif score >= 32: return "✅ Recommended"
                        elif score >= 22: return "⚠️ Review Needed"
                        else: return "❌ Not a Match"
                    
                    df["remark"] = df["score"].apply(get_remark)
                    
                    # --- FEATURE 1: VISUAL LEADERBOARD ---
                    st.subheader("📊 Leaderboard")
                    
                    # Bar Chart
                    st.bar_chart(df.set_index("filename")["score"], color="#0d9488")
                    
                    # --- FEATURE 2: DETAILED TABLE WITH GAP ANALYSIS ---
                    st.subheader("📝 Detailed Analysis")
                    
                    # Formatting the dataframe for display
                    # Added "remark" column here
                    display_df = df[["rank", "filename", "score", "remark", "feedback"]]
                    
                    # Apply color gradient to scores
                    st.dataframe(
                        display_df.style.background_gradient(subset=['score'], cmap="RdYlGn"),
                        width='stretch',
                        column_config={
                            "rank": "Rank",
                            "filename": "Candidate Name",
                            "score": st.column_config.ProgressColumn(
                                "Match Score",
                                help="AI-calculated relevance score",
                                format="%.2f%%",
                                min_value=0,
                                max_value=100,
                            ),
                            "remark": "AI Verdict",
                            "feedback": "Skill Gap Analysis"
                        }
                    )

                    # --- FEATURE 3: EXPORT RESULTS ---
                    csv = display_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Ranking Report (CSV)",
                        data=csv,
                        file_name="candidate_ranking.csv",
                        mime="text/csv",
                    )
                    
                else:
                    st.error("Backend Error. Check logs.")
                    
            except Exception as e:
                st.error(f"Connection Failed: {e}")