from src.skill_matching import get_user_skills, get_matched_skills, normalize_user_input

def test_aliases_are_normalized():
    text = normalize_user_input("AI ML CV")
    assert "artificial intelligence" in text
    assert "machine learning" in text
    assert "computer vision" in text

def test_multiple_skills_detected():
    skills = get_user_skills("Python Machine Learning Computer Vision Agriculture")
    assert "python" in skills
    assert "machine learning" in skills
    assert "computer vision" in skills
    assert "agriculture" in skills

def test_phrase_matching_does_not_match_partial_words():
    matches = get_matched_skills("AI", "The mailing system is ready")
    assert "machine learning" not in matches
