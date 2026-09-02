import numpy as np
from src.validation import validate_user_query, is_query_relevant, filter_relevant_candidates

def test_empty_query_is_invalid():
    valid, message = validate_user_query("   ")
    assert not valid
    assert message

def test_valid_query():
    valid, message = validate_user_query("Python Machine Learning")
    assert valid
    assert message == ""

def test_unknown_query_without_similarity_is_not_relevant():
    relevant, confidence = is_query_relevant("BGMI", np.array([0.0, 0.001]))
    assert not relevant
    assert confidence["recognized_skills"] == []

def test_known_skill_is_relevant():
    relevant, confidence = is_query_relevant("Machine Learning", np.array([0.0, 0.001]))
    assert relevant
    assert "machine learning" in confidence["recognized_skills"]

def test_candidate_filter_removes_irrelevant_rows():
    candidates = [
        {"similarity": 0.0, "matched_skills": [], "theme_matches": []},
        {"similarity": 0.0, "matched_skills": ["python"], "theme_matches": []},
    ]
    filtered = filter_relevant_candidates(candidates)
    assert len(filtered) == 1
    assert filtered[0]["matched_skills"] == ["python"]
