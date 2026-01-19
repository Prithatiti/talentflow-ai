# backend/routers/resumes.py

import os
import shutil
import faiss
import numpy as np
from typing import List
from logger import logger
from fastapi import APIRouter, UploadFile, File, Form
from utils import extract_text_from_pdf, query_groq
from services import get_embedder

router = APIRouter()
embedder = get_embedder()

@router.post("/screen_resumes")
async def screen_resumes(
    jd_text: str = Form(...),
    files: List[UploadFile] = File(...)
):
    logger.info(f"Resume Screening Started. Received {len(files)} files.")

    # --- STEP 1: Smart Keyword Extraction (New Feature) ---
    # We ask Groq to extract key technical skills from the JD to check for gaps later.
    try:
        skill_prompt = f"""
        Extract the top 5-10 essential technical skills from this Job Description. 
        Output strictly as a comma-separated list (e.g., Python, AWS, Docker). 
        No other text.
        
        JD: {jd_text[:2000]}
        """
        # We use Groq for speed
        extracted_skills_str = query_groq(skill_prompt)
        # Clean up list
        required_skills = [s.strip().lower() for s in extracted_skills_str.split(',') if s.strip()]
        logger.info(f"Extracted Skills for Gap Analysis: {required_skills}")
    except Exception as e:
        logger.error(f"Skill extraction failed: {e}")
        required_skills = []

    # --- STEP 2: Process Resumes & Embed ---
    resume_data = [] # Store text and filename
    
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    
    for file in files:
        file_path = os.path.join(temp_dir, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
            
        try:
            text = extract_text_from_pdf(file_path)
            if text.strip():
                resume_data.append({"filename": file.filename, "text": text})
        except:
            continue
            
    # Cleanup early
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    if not resume_data:
        return {"results": []}

    # --- STEP 3: Vector Search (The Math) ---
    # Batch encode
    resume_texts = [r["text"] for r in resume_data]
    resume_embeddings = embedder.encode(resume_texts)
    jd_embedding = embedder.encode([jd_text])

    # Normalize
    faiss.normalize_L2(np.array(jd_embedding))
    faiss.normalize_L2(np.array(resume_embeddings))

    # Index
    d = resume_embeddings.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(np.array(resume_embeddings))
    
    # Search
    distances, indices = index.search(np.array(jd_embedding), len(resume_data))
    
    # --- STEP 4: Compile Results with Gap Analysis ---
    results = []
    
    for rank, idx in enumerate(indices[0]):
        similarity = distances[0][rank]
        score = float(similarity * 100)
        
        # New Feature: Identify Missing Skills
        resume_text_lower = resume_texts[idx].lower()
        missing = [skill for skill in required_skills if skill not in resume_text_lower]
        
        # Create a "Match Reason" summary
        if len(missing) == 0:
            feedback = "Perfect Skill Match!"
        elif len(missing) > 3:
            feedback = f"Missing key skills: {', '.join(missing[:3])}, etc."
        else:
            feedback = f"Missing: {', '.join(missing)}"

        results.append({
            "rank": rank + 1,
            "filename": resume_data[idx]["filename"],
            "score": round(score, 2),
            "score_formatted": f"{round(score, 2)}%",  # Explicit percentage string
            "missing_skills": missing,
            "feedback": feedback,
            "summary": resume_texts[idx][:200] + "..." # Preview
        })

    # Sort by score desc (Just to be safe, though FAISS returns sorted)
    results.sort(key=lambda x: x['score'], reverse=True)
    
    return {"results": results}