# backend/services.py

from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL
from logger import logger

# Singleton Pattern: Load model only once when the app starts
logger.info("Loading Embedding Model...")
embedder = SentenceTransformer(EMBEDDING_MODEL)
logger.info("Model Loaded.")

def get_embedder():
    return embedder
