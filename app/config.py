import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

VECTOR_PATH = BASE_DIR / "models" / "sih_tfidf_vectorizer.pkl"
MATRIX_PATH = BASE_DIR / "models" / "sih_tfidf_matrix.pkl"
DATASET_PATH = BASE_DIR / "data" / "processed" / "sih_recommendation_dataset.csv"

DEBUG = os.getenv("FLASK_DEBUG", "0").lower() in {"1", "true", "yes"}
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "5000"))

SECRET_KEY = os.getenv("SECRET_KEY")
MAX_CONTENT_LENGTH = 16 * 1024

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = not DEBUG
