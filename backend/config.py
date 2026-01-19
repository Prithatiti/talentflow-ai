# backend/config.py

import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Server Settings
HOST = "0.0.0.0"
PORT = 8000

# AI Configuration
# We use os.getenv to safely read from the .env file

# Gemini (Main App)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash") # Default if not found


# Groq Config
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile") # Default if not found


# Local Embeddings (Fast & Free)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# Ollama Settings (Optional fallback)
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:1b"