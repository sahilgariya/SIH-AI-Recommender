from src.skill_matching import (
    get_user_skills,
    get_matched_skills,
    get_skill_coverage
)


def test_get_user_skills():

    user_input = (
        "Python Machine Learning "
        "Computer Vision Agriculture"
    )

    skills = get_user_skills(
        user_input
    )

    assert "python" in skills

    assert "machine learning" in skills

    assert "computer vision" in skills

    assert "agriculture" in skills


def test_get_matched_skills():

    user_input = (
        "Python Machine Learning "
        "Agriculture"
    )

    problem_text = (
        "Develop a machine learning "
        "system for agriculture."
    )

    matched_skills = (
        get_matched_skills(
            user_input,
            problem_text
        )
    )

    assert "machine learning" in matched_skills

    assert "agriculture" in matched_skills


def test_get_skill_coverage():

    user_input = (
        "Python Machine Learning "
        "Computer Vision Agriculture"
    )

    problem_text = (
        "Machine learning and computer "
        "vision for agriculture."
    )

    coverage = (
        get_skill_coverage(
            user_input,
            problem_text
        )
    )

    assert coverage == 0.75


def test_empty_user_input():

    skills = get_user_skills(
        ""
    )

    assert skills == []