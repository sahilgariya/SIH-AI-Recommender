"""
Hybrid scoring system.
"""

from .skill_matching import get_matched_skills, get_skill_coverage

DOMAINS = [
    "agriculture", "health", "education", "robotics", "cybersecurity",
    "space", "environment", "smart automation", "transportation",
]

GENERIC_TITLES = {"student innovation", "innovation"}


def _text(value):
    return "" if value is None else str(value).lower()


def get_theme_match(user_input, problem):
    user_text = _text(user_input)
    searchable = " ".join([
        _text(problem.get("Theme", "")),
        _text(problem.get("Details", "")),
        _text(problem.get("weighted_text", "")),
    ])
    return [
        domain for domain in DOMAINS
        if domain in user_text and domain in searchable
    ]


def calculate_final_score(user_input, problem, similarity_score):
    title = _text(problem.get("Problem Statement Title", ""))
    theme = _text(problem.get("Theme", ""))
    problem_text = _text(problem.get("weighted_text", ""))

    final_score = max(0.0, float(similarity_score)) * 100.0
    matched_skills = get_matched_skills(user_input, problem_text)

    for skill in matched_skills:
        if skill in title:
            final_score += 8
        elif skill in theme:
            final_score += 5
        else:
            final_score += 3

    final_score += get_skill_coverage(user_input, problem_text) * 12
    final_score += len(get_theme_match(user_input, problem)) * 6

    if title.strip() in GENERIC_TITLES:
        final_score -= 8

    return max(0.0, final_score)
