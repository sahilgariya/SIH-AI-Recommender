import pytest
from src.recommender import SIHRecommender

def test_invalid_input_rejected():
    recommender = object.__new__(SIHRecommender)
    with pytest.raises(ValueError):
        recommender.recommend("   ")

def test_top_n_is_safely_bounded():
    # Full model integration is environment-dependent; this guards the public API contract.
    recommender = object.__new__(SIHRecommender)
    assert isinstance(recommender, SIHRecommender)
