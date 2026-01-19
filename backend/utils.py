# backend/utils.py

import requests
from PyPDF2 import PdfReader
from google import genai
from groq import Groq
from config import (
    GEMINI_API_KEY, GEMINI_MODEL,
    OLLAMA_URL, MODEL_NAME, 
    GROQ_API_KEY, GROQ_MODEL
)


# --- 1. GEMINI CLIENT ---
try:
    gemini_client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    print(f"Gemini Init Error: {e}")
    gemini_client = None

# --- 2. GROQ CLIENT ---
try:
    groq_client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    print(f"Groq Init Error: {e}")
    groq_client = None


# --- FUNCTIONS ---
def query_gemini(prompt: str):
    if not gemini_client:
        return "Gemini Client Error"
    try:
        response = gemini_client.models.generate_content(
            model=GEMINI_MODEL, contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Gemini Error: {str(e)}"
    

def query_groq(prompt: str):
    """
    Queries the Groq API for ultra-fast inference.
    """
    if not groq_client:
        return "Groq Client Error: Check API Key"
    
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=GROQ_MODEL,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Groq API Error: {str(e)}"
    

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