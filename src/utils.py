# Utility/helper functions
"""
Utility and helper functions.
"""


def validate_user_input(
    user_input
):
    """
    Check whether the user entered
    a valid recommendation query.
    """

    if user_input is None:

        return False

    user_input = str(
        user_input
    ).strip()

    if len(user_input) == 0:

        return False

    return True


def create_reason(
    matched_skills,
    theme_matches
):
    """
    Create a human-readable explanation
    for why a problem was recommended.
    """

    reasons = []

    if matched_skills:

        skill_text = (
            "Matching Skills: "
            + ", ".join(
                matched_skills
            )
        )

        reasons.append(
            skill_text
        )


    if theme_matches:

        theme_text = (
            "Matching Theme/Domain: "
            + ", ".join(
                theme_matches
            )
        )

        reasons.append(
            theme_text
        )


    if not reasons:

        reasons.append(
            "Recommended based on overall "
            "text similarity."
        )


    return " | ".join(
        reasons
    )


def safe_text(
    value
):
    """
    Safely convert values into text.
    """

    if value is None:

        return ""

    return str(
        value
    ).strip()