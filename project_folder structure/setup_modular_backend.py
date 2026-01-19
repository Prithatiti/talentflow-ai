import os

# Define the modular structure
structure = {
    "backend": {
        "__init__.py": "",
        
        # 1. CONFIGURATION
        "config.py": """
import os

# Server Settings
HOST = "0.0.0.0"
PORT = 8000

# AI Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen3:4b"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
""",

        # 2. DATA MODELS (SCHEMAS)
        "schemas.py": """
from pydantic import BaseModel

class JDRequest(BaseModel):
    role: str
    skills: str
    experience: str

class ChatRequest(BaseModel):
    history: str
    message: str
    context: str
""",

        # 3. HELPER FUNCTIONS
        "utils.py": """
import requests
from PyPDF2 import PdfReader
from .config import OLLAMA_URL, MODEL_NAME

def query_ollama(prompt: str):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        return response.json().get('response', "Error from Ollama")
    except Exception as e:
        return f"Ollama Connection Error: {str(e)}"

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
""",

        # 4. SERVICES (AI LOADER)
        "services.py": """
from sentence_transformers import SentenceTransformer
from .config import EMBEDDING_MODEL

# Singleton Pattern: Load model only once when the app starts
print("Loading Embedding Model...")
embedder = SentenceTransformer(EMBEDDING_MODEL)
print("Model Loaded.")

def get_embedder():
    return embedder
""",

        # 5. ROUTERS (API ENDPOINTS)
        "routers": {
            "__init__.py": "",
            
            # --- JD GENERATOR ROUTER ---
            "jobs.py": """
from fastapi import APIRouter
from backend.schemas import JDRequest
from backend.utils import query_ollama

router = APIRouter()

@router.post("/generate_jd")
async def generate_jd(req: JDRequest):
    prompt = f\"\"\"
        Generate a concise and professional Job Description for the role of {req.role}.

        Follow this exact format:

        Job Title:
        Role Overview: (2–3 lines summary)
        Key Responsibilities:
        - Bullet points only
        Qualifications:
        - Bullet points only

        Requirements:
        - Required skills: {req.skills}
        - Experience: {req.experience}+ years
    \"\"\"
    jd_text = query_ollama(prompt)
    return {"jd": jd_text}
""",

            # --- RESUME SCREENER ROUTER ---
            "resumes.py": """
import os
import shutil
import faiss
import numpy as np
from typing import List
from fastapi import APIRouter, UploadFile, File, Form
from backend.utils import extract_text_from_pdf
from backend.services import get_embedder

router = APIRouter()
embedder = get_embedder()

@router.post("/screen_resumes")
async def screen_resumes(
    jd_text: str = Form(...),
    files: List[UploadFile] = File(...)
):
    # 1. Embed JD
    jd_embedding = embedder.encode([jd_text])
    
    # 2. Process Resumes
    resume_texts = []
    filenames = []
    
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    
    for file in files:
        file_path = os.path.join(temp_dir, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
            
        try:
            text = extract_text_from_pdf(file_path)
            if text.strip():
                resume_texts.append(text)
                filenames.append(file.filename)
        except:
            continue

    if not resume_texts:
        return {"results": []}

    # 3. Embed Resumes
    resume_embeddings = embedder.encode(resume_texts)

    # 4. FAISS Search
    dimension = resume_embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(resume_embeddings))
    
    # Search for resumes closest to JD
    k = len(resume_texts) 
    distances, indices = index.search(np.array(jd_embedding), k)
    
    results = []
    for i, idx in enumerate(indices[0]):
        # Convert L2 distance to a similarity score (0-100 approximation)
        raw_score = 100 - (distances[0][i] * 50)
        score = float(max(0, raw_score))
        
        results.append({
            "filename": filenames[idx],
            "score": round(score, 2),
            "summary": resume_texts[idx][:200] + "..." 
        })

    # Cleanup
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
    # Sort by score desc
    results.sort(key=lambda x: x['score'], reverse=True)
    return {"results": results}
""",

            # --- INTERVIEW ROUTER ---
            "interview.py": """
from fastapi import APIRouter
from backend.schemas import ChatRequest
from backend.utils import query_ollama

router = APIRouter()

@router.post("/interview_bot")
async def interview_bot(req: ChatRequest):
    system_instruction = f\"\"\"
        You are a professional technical recruiter conducting a preliminary screening interview.

        Context:
        - Job Description (JD): {req.context}
        - Chat History: {req.history}
        - Candidate Message: {req.message}

        Interview Rules:
        1. If the candidate says "START_INTERVIEW":
        - Briefly introduce yourself (1 line).
        - Ask the FIRST, EASY technical question strictly based on the JD.

        2. If the candidate answers a question:
        - Mentally assess correctness and confidence.
        - If the answer is reasonable, ask the NEXT question with slightly higher complexity.
        - If the answer is weak or incorrect, ask a DIFFERENT easy or medium-level question from another JD-relevant concept.

        3. If the candidate says phrases like:
        - "I don't know", "Not sure", "No idea"
        - or clearly indicates lack of knowledge
        - Do NOT probe further on the same concept.
        - Switch to a DIFFERENT concept from the JD and ask an EASIER question.

        Strict Constraints:
        - Ask ONLY ONE technical question at a time.
        - Do NOT ask follow-up or multi-part questions.
        - Do NOT explain answers or give hints.
        - Keep questions concise and recruiter-style.
        - Increase difficulty gradually only when the candidate demonstrates competence.
        - All questions must be strictly grounded in the Job Description and prior responses.

        Response Format (must follow exactly):
        Interviewer Question:
    \"\"\"
    
    response = query_ollama(system_instruction)
    return {"reply": response}
"""
        },

        # 6. MAIN ENTRY POINT
        "main.py": """
import uvicorn
from fastapi import FastAPI
from backend.config import HOST, PORT
from backend.routers import jobs, resumes, interview

app = FastAPI(title="Recruiter AI Backend")

# Include Routers
app.include_router(jobs.router)
app.include_router(resumes.router)
app.include_router(interview.router)

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host=HOST, port=PORT, reload=True)
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
print("\\n✅ Modular Backend Created Successfully!")

"""


### **3. How to Run the Modular Version**

1.  **Generate Files:**
    Run the script above:
    ```bash
    python setup_modular_backend.py
    ```
2.  **Start the Server:**
    Run the following command from the **root** folder (the folder containing the `backend` directory):
    ```bash
    python -m backend.main
    ```
    *(Note: Using `-m backend.main` ensures Python understands the imports correctly).*

3.  **Frontend:**
    No changes are needed for the frontend. You can just run it as usual:
    ```bash
    streamlit run frontend/app.py
    ```
"""