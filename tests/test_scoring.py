from src.scoring import calculate_final_score, get_theme_match

def test_skill_match_increases_score():
    problem = {
        "Problem Statement Title": "Machine Learning for Agriculture",
        "Theme": "Agriculture, FoodTech & Rural Development",
        "Details": "Use machine learning to solve agriculture problems.",
        "weighted_text": "machine learning agriculture python"
    }
    score = calculate_final_score("Python Machine Learning Agriculture", problem, 0.10)
    assert score > 10

def test_theme_matching():
    problem = {
        "Theme": "Robotics and Drones",
        "Details": "Computer vision based autonomous robotics",
        "weighted_text": "robotics computer vision"
    }
    matches = get_theme_match("Computer Vision Robotics", problem)
    assert "robotics" in matches
