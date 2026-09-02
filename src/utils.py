"""
Utility functions.
"""

import math


def validate_user_input(user_input):
    return user_input is not None and bool(str(user_input).strip())


def safe_text(value):
    if value is None:
        return ""
    try:
        if math.isnan(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value).strip()


def create_reason(matched_skills, theme_matches):
    reasons = []
    if matched_skills:
        reasons.append("Matching Skills: " + ", ".join(matched_skills))
    if theme_matches:
        reasons.append(
            "Matching Theme/Domain: " + ", ".join(theme_matches)
        )
    return " | ".join(reasons) if reasons else "Recommended based on measurable text similarity."
