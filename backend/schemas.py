# backend/schemas.py

from pydantic import BaseModel

class JDRequest(BaseModel):
    role: str
    skills: str
    experience: str

class ChatRequest(BaseModel):
    history: str
    message: str
    context: str
