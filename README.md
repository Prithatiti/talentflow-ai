# 👔 Talentflow AI: The Recruiter's Intelligent Assistant

**Talentflow AI** is an end-to-end intelligent application designed to accelerate the corporate hiring cycle. By leveraging **Semantic Search (Vector Embeddings)** and **Generative AI (LLMs)**, it automates the most repetitive tasks in recruitment: screening resumes, generating job descriptions, and conducting preliminary interviews.

---

## 🛠️ Technical Architecture

<p align="center">
  <img src=".\architecture diagram\Talentflow_AI Architectural Diagram.png" alt="TalentFlow AI Architecture" width="100%">
</p>

---

## 🚀 Key Features

### 1. 🔍 Smart Resume Screening
* **Semantic Matching:** Uses **FAISS** and `all-MiniLM-L6-v2` to rank candidates based on conceptual meaning, not just keyword matching.
* **Skill Gap Analysis:** Automatically detects missing technical skills (e.g., *"Candidate has Python but lacks Docker"*) and provides a verdict.
* **Visual Leaderboard:** Dynamic charts and color-coded feedback allow for instant decision-making.

### 2. 📝 Intelligent JD Generator
* **One-Click Drafts:** Generates professional, structured Job Descriptions using **Groq (Llama 3)**.
* **Standardized Format:** Ensures all JDs follow a consistent corporate structure (Role, Responsibilities, Requirements).

### 3. 🤖 AI Preliminary Interviewer
* **Context-Aware:** Conducts a technical chat with candidates based strictly on the specific JD.
* **Adaptive Logic:** Adjusts question difficulty based on the candidate's answers.
* **Hallucination Safety:** Uses strict "Negative Constraints" to prevent the AI from giving hints.

### 4. 📊 Evaluation & Quality Assurance
* **Golden Resume Test:** A diagnostic unit test that injects the JD text as a resume to verify the embedding model's integrity.
* **LLM-as-a-Judge:** Uses **Gemini 2.5** to audit interview transcripts and grade the AI recruiter on relevance and professionalism.

---

## 🛠️ Technical Architecture

### Tech Stack
* **Frontend:** Streamlit (Custom CSS for Dashboard UI)
* **Backend:** FastAPI (Async Python Server)
* **AI Orchestration:**
    * **Generation:** Groq (Llama-3.3-70b), Google Gemini 2.5 Flash
    * **Embeddings:** HuggingFace `sentence-transformers/all-MiniLM-L6-v2`
* **Vector Database:** FAISS (Local, In-memory)
* **Data Processing:** PyPDF2, Pandas

### System Flow
1.  **User Upload:** Recruiter uploads PDFs via Streamlit.
2.  **Vectorization:** Backend converts text to vectors using HuggingFace models.
3.  **Storage:** Vectors are indexed in FAISS.
4.  **Retrieval:** System calculates Cosine Similarity between JD and Resumes.
5.  **Generation:** LLMs handle chat interactions and JD drafting.

---

## 💻 Installation & Setup

### Prerequisites
* Python 3.9 or higher
* API Keys for **Groq** and **Google Gemini**

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/talentflow-ai.git](https://github.com/your-username/talentflow-ai.git)
cd talentflow-ai
```

---

### 2. Set Up Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

---
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---
### 4. Configure Environment Variables
```bash
Create a .env file in the backend/ directory:

GEMINI_API_KEY=your_gemini_key_here
GROQ_API_KEY=your_groq_key_here
```

---
### 5. Run the Application
```bash
You need to run the Backend and Frontend in separate terminals.

Terminal 1: Backend

cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000


Terminal 2: Frontend

cd frontend
streamlit run app.py


Access the app at: http://localhost:8501
```
## 📂 Project Structure

```
talentflow-ai/
├── backend/
│   ├── main.py           # FastAPI Entry Point
│   ├── config.py         # Env Config
│   ├── routers/          # API Endpoints (Jobs, Resumes, Interview)
│   ├── services.py       # Embedding Logic
│   └── utils.py          # LLM Client Wrappers
├── frontend/
│   ├── app.py            # Streamlit Entry Point
│   ├── views/            # UI Pages (Screener, Generator, Home)
│   └── styles.py         # Custom CSS
└── requirements.txt      # Python Dependencies
```

---

## 🛡️ Quality Assurance (The "Golden Resume")

To prove the reliability of the system, we implemented the Golden Resume Test.

Logic: We inject the JD text itself into the candidate pool.

Success Condition: The JD-as-a-Resume must rank #1 with a 100% match score.

Result: This proves the embedding model is capturing semantic meaning correctly.

---

## 🔮 Future Scope

Video Interview Analysis: Analyzing candidate confidence via video feed.

ATS Integration: Direct connection to LinkedIn/Greenhouse.

Multi-Language Support: Interviewing candidates in their native language.

---

## 👨‍💻 Author

Pritha Majumder Capstone Project 2026
