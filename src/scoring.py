"""
Hybrid scoring system.
"""


from .skill_matching import (
    get_user_skills,
    get_matched_skills
)


DOMAINS = [

    "agriculture",

    "health",

    "education",

    "robotics",

    "cybersecurity",

    "space",

    "environment",

    "smart automation",

    "transportation"
]


def get_theme_match(
    user_input,
    problem
):
    """
    Check whether user interests match
    the SIH problem theme.
    """

    user_text = str(
        user_input
    ).lower()

    theme = str(
        problem.get(
            "Theme",
            ""
        )
    ).lower()

    matched_domains = []

    for domain in DOMAINS:

        if (
            domain in user_text
            and
            domain in theme
        ):

            matched_domains.append(
                domain
            )

    return matched_domains


def calculate_final_score(
    user_input,
    problem,
    similarity_score
):
    """
    Calculate final hybrid recommendation score.

    Formula:

    TF-IDF Similarity
    +
    Skill Match Bonus
    +
    Multi-Skill Coverage Bonus
    +
    Theme Match Bonus
    -
    Generic Title Penalty
    """

    problem_title = str(
        problem.get(
            "Problem Statement Title",
            ""
        )
    ).lower()

    problem_theme = str(
        problem.get(
            "Theme",
            ""
        )
    ).lower()

    problem_text = str(
        problem.get(
            "weighted_text",
            ""
        )
    ).lower()

    # Base TF-IDF score
    final_score = (
        float(similarity_score)
        * 100
    )

    # Detect user skills
    user_skills = get_user_skills(
        user_input
    )

    # Find matching skills
    matched_skills = get_matched_skills(
        user_input,
        problem_text
    )

    # Add skill bonuses
    for skill in matched_skills:

        # Highest importance:
        # skill appears in title
        if skill in problem_title:

            final_score += 12

        # Medium importance:
        # skill appears in theme
        elif skill in problem_theme:

            final_score += 8

        # Normal importance:
        # skill appears in description
        else:

            final_score += 4


    # Multi-skill coverage bonus
    if len(user_skills) > 0:

        coverage = (
            len(matched_skills)
            / len(user_skills)
        )

        final_score += (
            coverage * 20
        )


    # Theme/domain bonus
    theme_matches = get_theme_match(
        user_input,
        problem
    )

    final_score += (
        len(theme_matches)
        * 10
    )


    # Generic title penalty
    generic_titles = [

        "student innovation",

        "innovation"
    ]

    if (
        problem_title.strip()
        in generic_titles
    ):

        final_score -= 10


    return final_score