# backend/routers/evaluate.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import numpy as np
import faiss
from services import get_embedder
from utils import query_gemini, query_ollama, query_groq


router = APIRouter()
embedder = get_embedder()


class JDEvalRequest(BaseModel):
    jd_text: str
    required_skills: str

class ScreenerEvalRequest(BaseModel):
    jd_text: str
    resume_texts: List[str] # We will send the text of uploaded resumes to test

class InterviewEvalRequest(BaseModel):
    history: str
    jd_context: str


# 1. Evaluate JD Generator (Keyword Recall)
@router.post("/evaluate_jd")
async def evaluate_jd(req: JDEvalRequest):
    # Logic: Check how many requested skills are actually present in the generated JD
    skills_list = [s.strip().lower() for s in req.required_skills.split(",")]
    jd_lower = req.jd_text.lower()
    
    found = []
    missing = []
    
    for skill in skills_list:
        if skill in jd_lower:
            found.append(skill)
        else:
            missing.append(skill)
            
    score = (len(found) / len(skills_list)) * 100 if skills_list else 0
    
    return {
        "score": round(score, 2),
        "found": found,
        "missing": missing,
        "verdict": "Excellent" if score > 80 else "Needs Improvement"
    }


# 2. Evaluate Screener (The 'Golden Resume' Test)
@router.post("/evaluate_screener")
async def evaluate_screener(req: ScreenerEvalRequest):
    # Logic: Inject the JD text itself as a "Golden Resume". 
    # It SHOULD be the #1 match (Score ~100%). If not, the model is broken.
    
    texts = req.resume_texts.copy()
    texts.append(req.jd_text) # Inject Golden Resume at the end
    
    embeddings = embedder.encode(texts)
    jd_embedding = embedder.encode([req.jd_text])
    
    # Normalize for Cosine Similarity
    faiss.normalize_L2(np.array(embeddings))
    faiss.normalize_L2(np.array(jd_embedding))
    
    d = embeddings.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(np.array(embeddings))
    
    # Search
    D, I = index.search(np.array(jd_embedding), len(texts))
    
    # Find where the Golden Resume (last index) landed
    golden_index = len(texts) - 1
    rank_of_golden = -1
    score_of_golden = 0.0
    
    for rank, idx in enumerate(I[0]):
        if idx == golden_index:
            rank_of_golden = rank + 1 # 1-based ranking
            score_of_golden = float(D[0][rank]) * 100
            break
            
    return {
        "integrity_check": "PASSED" if rank_of_golden == 1 else "FAILED",
        "golden_resume_rank": rank_of_golden,
        "golden_resume_score": round(score_of_golden, 2),
        "explanation": "We injected the JD text as a resume. It ranked #" + str(rank_of_golden) + ". Ideally, it should be #1."
    }


# 3. Evaluate Interviewer (LLM-as-a-Judge)
@router.post("/evaluate_interview")
async def evaluate_interview(req: InterviewEvalRequest):
    # Logic: Ask Gemini to grade the chat history
    prompt = f"""
    You are a Senior Hiring Manager auditing an AI Recruiter.
    
    Job Description: {req.jd_context}
    
    Interview Transcript:
    {req.history}
    
    Task: Evaluate the AI Interviewer's performance.
    1. Relevance (1-10): Did the AI ask questions relevant to the JD?
    2. Professionalism (1-10): Was the tone appropriate?
    3. Flow (1-10): Did the conversation flow logically?
    
    Output JSON format only:
    {{
        "relevance_score": 0,
        "professionalism_score": 0,
        "flow_score": 0,
        "feedback": "Short summary of feedback"
    }}
    """
    
    try:
        # feedback = query_ollama(prompt)
        # feedback = query_gemini(prompt)
        feedback = query_groq(prompt)
        feedback = feedback.replace("```json", "").replace("```", "")
        return {"report": feedback}
    
    except Exception as e:
        return {"error": str(e)}