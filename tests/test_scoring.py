from src.scoring import (
    get_theme_match,
    calculate_final_score
)


def create_test_problem():

    problem = {

        "Problem Statement Title":
        (
            "Machine Learning System "
            "for Agriculture"
        ),

        "Theme":
        (
            "Agriculture, FoodTech & "
            "Rural Development"
        ),

        "Category":
        "Software",

        "weighted_text":
        (
            "Machine learning system "
            "using python and computer "
            "vision for agriculture."
        )
    }

    return problem


def test_theme_match():

    user_input = (
        "Python Machine Learning Agriculture"
    )

    problem = create_test_problem()

    matches = get_theme_match(
        user_input,
        problem
    )

    assert "agriculture" in matches


def test_final_score():

    user_input = (
        "Python Machine Learning Agriculture"
    )

    problem = create_test_problem()

    similarity_score = 0.50

    final_score = (
        calculate_final_score(
            user_input,
            problem,
            similarity_score
        )
    )

    # Score should be higher
    # than base TF-IDF score
    assert final_score > 50


def test_generic_title_penalty():

    user_input = (
        "Machine Learning Agriculture"
    )

    generic_problem = {

        "Problem Statement Title":
        "Student Innovation",

        "Theme":
        "Agriculture",

        "Category":
        "Software",

        "weighted_text":
        (
            "Machine learning "
            "agriculture project"
        )
    }

    score = (
        calculate_final_score(
            user_input,
            generic_problem,
            0.50
        )
    )

    assert score > 0


def test_score_returns_number():

    problem = create_test_problem()

    score = (
        calculate_final_score(
            "Machine Learning",
            problem,
            0.40
        )
    )

    assert isinstance(
        score,
        float
    )