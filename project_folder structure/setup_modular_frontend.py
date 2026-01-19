import os

# Define the modular frontend structure
structure = {
    "frontend": {
        # 1. CONFIGURATION
        "config.py": """
import os

# Backend API URL
API_URL = "http://localhost:8000"

# Page Configuration
PAGE_TITLE = "Recruiter AI"
PAGE_ICON = "👔"
LAYOUT = "wide"
""",

        # 2. CUSTOM CSS STYLES
        "styles.py": """
import streamlit as st

def load_css():
    st.markdown(\"\"\"
        <style>
        .main {
            background-color: #f8f9fa;
        }
        .stButton>button {
            background-color: #007bff;
            color: white;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            border: none;
        }
        .stButton>button:hover {
            background-color: #0056b3;
        }
        .card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        </style>
    \"\"\", unsafe_allow_html=True)
""",

        # 3. VIEWS (PAGES)
        "views": {
            "__init__.py": "",

            # --- JD GENERATOR PAGE ---
            "generator.py": """
import streamlit as st
import requests
from frontend.config import API_URL

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
""",

            # --- RESUME SCREENER PAGE ---
            "screener.py": """
import streamlit as st
import requests
import pandas as pd
from frontend.config import API_URL

def render_screener():
    st.title("🔍 AI Resume Screening")
    st.markdown("Rank resumes against Job Descriptions using Vector Similarity (FAISS).")
    
    jd_input = st.text_area("Paste Job Description (or generate one)", 
                           value=st.session_state.get('generated_jd', ""), height=150)
    
    uploaded_files = st.file_uploader("Upload Resumes (PDF)", type=["pdf"], accept_multiple_files=True)
    
    if st.button("Screen Resumes") and uploaded_files and jd_input:
        with st.spinner("Processing PDF embeddings..."):
            files = [('files', (f.name, f, 'application/pdf')) for f in uploaded_files]
            try:
                res = requests.post(f"{API_URL}/screen_resumes", data={"jd_text": jd_input}, files=files)
                if res.status_code == 200:
                    results = res.json().get("results")
                    
                    if results:
                        df = pd.DataFrame(results)
                        st.markdown("### 🏆 Ranking Results")
                        st.dataframe(
                            df.style.background_gradient(subset=['score'], cmap="Greens"),
                            use_container_width=True
                        )
                    else:
                        st.warning("No readable text found in PDFs.")
                else:
                    st.error("Backend Error.")
            except Exception as e:
                st.error(f"Failed: {e}")
""",

            # --- AI INTERVIEW PAGE ---
            "interview.py": """
import streamlit as st
import requests
from frontend.config import API_URL

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
                history_str = "\\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
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
"""
        },

        # 4. MAIN ENTRY POINT
        "app.py": """
import streamlit as st
from frontend.config import PAGE_TITLE, PAGE_ICON, LAYOUT
from frontend.styles import load_css
from frontend.views.generator import render_generator
from frontend.views.screener import render_screener
from frontend.views.interview import render_interview

# 1. Config
st.set_page_config(page_title=PAGE_TITLE, layout=LAYOUT, page_icon=PAGE_ICON)

# 2. Load CSS
load_css()

# 3. Sidebar Navigation
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("Recruiter AI")
    st.markdown("---")
    page = st.radio("Navigate", ["Job Description Generator", "Resume Screening", "AI Interviewer"])
    st.markdown("---")
    st.info("Powered by Qwen3:4b & FAISS")

# 4. Page Routing
if page == "Job Description Generator":
    render_generator()

elif page == "Resume Screening":
    render_screener()

elif page == "AI Interviewer":
    render_interview()
"""
    }
}

def create_structure(base_path, structure):
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        
        if isinstance(content, dict):
            create_structure(path, content)
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Created: {path}")

# Run creation logic
create_structure(".", structure)
print("\\n✅ Modular Frontend Created Successfully!")
"""

---

### **3. How to Run**

1.  **Generate the Frontend:**
    Run: `python setup_modular_frontend.py`

2.  **Run the App:**
    You still run the `app.py` file, but now it acts as a clean entry point that delegates logic to the other files.
    ```bash
    streamlit run frontend/app.py
    ```
"""