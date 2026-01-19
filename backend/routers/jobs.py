# backend/routers/jobs.py

from fastapi import APIRouter
from schemas import JDRequest
from utils import query_ollama, query_gemini, query_groq

router = APIRouter()

@router.post("/generate_jd")
async def generate_jd(req: JDRequest):
    prompt = f"""
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
    """
    
    # Use Ollama
    # jd_text = query_ollama(prompt)
    # Use Gemini
    jd_text = query_gemini(prompt)
    # Use Groq
    # jd_text = query_groq(prompt)

    return {"jd": jd_text}
