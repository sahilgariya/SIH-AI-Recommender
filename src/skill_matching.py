"""
Skill detection, normalization, query expansion, and skill matching.
"""

import re

SKILLS = [
    "python", "machine learning", "deep learning", "computer vision",
    "artificial intelligence", "data science", "data analysis",
    "natural language processing", "agriculture", "iot", "robotics",
    "blockchain", "cybersecurity", "cloud computing",
]

SKILL_ALIASES = {
    "ai": "artificial intelligence",
    "ml": "machine learning",
    "cv": "computer vision",
    "dl": "deep learning",
    "data analytics": "data analysis",
    "data analyst": "data analysis",
    "data scientist": "data science",
    "nlp": "natural language processing",
    "internet of things": "iot",
    "cyber security": "cybersecurity",
    "cloud": "cloud computing",
}


def _normalize_text(value):
    text = "" if value is None else str(value).lower()
    text = re.sub(r"[_/\\-]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _contains_phrase(text, phrase):
    return re.search(
        r"(?<!\w)" + re.escape(phrase) + r"(?!\w)",
        text,
    ) is not None


def normalize_user_input(user_input):
    text = _normalize_text(user_input)
    for alias, canonical in SKILL_ALIASES.items():
        text = re.sub(
            r"(?<!\w)" + re.escape(alias) + r"(?!\w)",
            canonical,
            text,
        )
    return re.sub(r"\s+", " ", text).strip()


def get_user_skills(user_input):
    text = normalize_user_input(user_input)
    return [
        skill for skill in SKILLS
        if _contains_phrase(text, skill)
    ]


def get_matched_skills(user_input, problem_text):
    text = _normalize_text(problem_text)
    return [
        skill for skill in get_user_skills(user_input)
        if _contains_phrase(text, skill)
    ]


def get_skill_coverage(user_input, problem_text):
    skills = get_user_skills(user_input)
    if not skills:
        return 0.0
    return len(get_matched_skills(user_input, problem_text)) / len(skills)


def expand_user_query(user_input):
    return normalize_user_input(user_input)
