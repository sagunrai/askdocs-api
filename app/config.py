"""Configuration loaded from environment variables."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    API_KEY = os.getenv("API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    CHROMA_PATH = os.getenv("CHROMA_PATH", "chroma_db")
    TOP_K = int(os.getenv("TOP_K", "4"))
    DATA_DIR = os.getenv("DATA_DIR", "data")


def require_keys():
    """Raise a clear error if required keys are missing."""
    missing = []
    if not Config.API_KEY:
        missing.append("API_KEY")
    if not Config.GEMINI_API_KEY:
        missing.append("GEMINI_API_KEY")
    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")