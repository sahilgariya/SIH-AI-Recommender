from pathlib import Path


# Project root folder
BASE_DIR = Path(__file__).resolve().parent.parent


# Model files
VECTOR_PATH = (
    BASE_DIR
    / "models"
    / "sih_tfidf_vectorizer.pkl"
)

MATRIX_PATH = (
    BASE_DIR
    / "models"
    / "sih_tfidf_matrix.pkl"
)


# Processed dataset
DATASET_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "sih_recommendation_dataset.csv"
)


# Application settings
DEBUG = True

HOST = "127.0.0.1"

PORT = 5000