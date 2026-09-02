from pathlib import Path

from src.recommender import (
    SIHRecommender
)


# Get project root folder
PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


VECTOR_PATH = (
    PROJECT_ROOT
    / "models"
    / "sih_tfidf_vectorizer.pkl"
)


MATRIX_PATH = (
    PROJECT_ROOT
    / "models"
    / "sih_tfidf_matrix.pkl"
)


DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "sih_recommendation_dataset.csv"
)


def test_recommender_loads():

    recommender = SIHRecommender(

        vectorizer_path=
        VECTOR_PATH,

        matrix_path=
        MATRIX_PATH,

        dataset_path=
        DATASET_PATH
    )

    assert recommender is not None


def test_recommendation_returns_results():

    recommender = SIHRecommender(

        vectorizer_path=
        VECTOR_PATH,

        matrix_path=
        MATRIX_PATH,

        dataset_path=
        DATASET_PATH
    )


    results = recommender.recommend(

        "Python Machine Learning "
        "Computer Vision Agriculture",

        top_n=10
    )


    assert len(results) == 10


def test_recommendation_result_structure():

    recommender = SIHRecommender(

        vectorizer_path=
        VECTOR_PATH,

        matrix_path=
        MATRIX_PATH,

        dataset_path=
        DATASET_PATH
    )


    results = recommender.recommend(

        "Machine Learning Agriculture",

        top_n=5
    )


    first_result = results[0]


    assert "rank" in first_result

    assert "ps_number" in first_result

    assert "title" in first_result

    assert "theme" in first_result

    assert "final_score" in first_result

    assert "matched_skills" in first_result

    assert "why_recommended" in first_result


def test_invalid_user_input():

    recommender = SIHRecommender(

        vectorizer_path=
        VECTOR_PATH,

        matrix_path=
        MATRIX_PATH,

        dataset_path=
        DATASET_PATH
    )


    try:

        recommender.recommend(
            "",
            top_n=10
        )

        assert False

    except ValueError:

        assert True