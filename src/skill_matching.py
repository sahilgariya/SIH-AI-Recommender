"""
Skill detection and skill matching functions.
"""


SKILLS = [

    "python",

    "machine learning",

    "deep learning",

    "computer vision",

    "artificial intelligence",

    "data science",

    "data analysis",

    "natural language processing",

    "nlp",

    "agriculture",

    "iot",

    "robotics",

    "blockchain",

    "cybersecurity",

    "cloud computing"
]


def get_user_skills(user_input):
    """
    Detect known skills from user input.
    """

    user_text = str(
        user_input
    ).lower()

    detected_skills = []

    for skill in SKILLS:

        if skill in user_text:

            detected_skills.append(
                skill
            )

    return detected_skills


def get_matched_skills(
    user_input,
    problem_text
):
    """
    Find user skills that match
    the SIH problem text.
    """

    user_skills = get_user_skills(
        user_input
    )

    problem_text = str(
        problem_text
    ).lower()

    matched_skills = []

    for skill in user_skills:

        if skill in problem_text:

            matched_skills.append(
                skill
            )

    return matched_skills


def get_skill_coverage(
    user_input,
    problem_text
):
    """
    Calculate the percentage of user
    skills matched by a problem.
    """

    user_skills = get_user_skills(
        user_input
    )

    if len(user_skills) == 0:

        return 0.0

    matched_skills = get_matched_skills(
        user_input,
        problem_text
    )

    coverage = (
        len(matched_skills)
        / len(user_skills)
    )

    return coverage