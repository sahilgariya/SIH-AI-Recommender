"""
Validation and confidence checks for recommendations.
"""

import numpy as np
from .skill_matching import get_user_skills

MIN_INPUT_LENGTH = 2
MIN_UNKNOWN_QUERY_SIMILARITY = 0.02
MIN_CANDIDATE_SIMILARITY = 0.02


def validate_user_query(user_input):
    text = "" if user_input is None else str(user_input).strip()
    if not text:
        return False, "Please enter at least one skill or interest."
    if len(text) < MIN_INPUT_LENGTH:
        return False, "Please enter a more specific skill or interest."
    if len(text) > 500:
        return False, "Please keep your input under 500 characters."
    return True, ""


def is_query_relevant(user_input, similarity_scores):
    scores = np.asarray(similarity_scores, dtype=float)
    max_similarity = float(np.max(scores)) if scores.size else 0.0
    skills = get_user_skills(user_input)

    confidence = {
        "max_similarity": max_similarity,
        "recognized_skills": skills,
    }

    if skills or max_similarity >= MIN_UNKNOWN_QUERY_SIMILARITY:
        return True, confidence

    return False, confidence


def filter_relevant_candidates(candidates):
    return [
        item for item in candidates
        if item.get("matched_skills")
        or item.get("theme_matches")
        or float(item.get("similarity", 0.0)) >= MIN_CANDIDATE_SIMILARITY
    ]
