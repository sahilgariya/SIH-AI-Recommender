"""
Main SIH AI Recommendation Engine.
"""

import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from .skill_matching import expand_user_query, get_matched_skills
from .scoring import calculate_final_score, get_theme_match
from .utils import create_reason, safe_text
from .validation import (
    filter_relevant_candidates,
    is_query_relevant,
    validate_user_query,
)


class SIHRecommender:
    def __init__(self, vectorizer_path, matrix_path, dataset_path):
        with open(vectorizer_path, "rb") as file:
            self.vectorizer = pickle.load(file)
        with open(matrix_path, "rb") as file:
            self.tfidf_matrix = pickle.load(file)

        self.df = pd.read_csv(dataset_path)

        if self.df.empty:
            raise ValueError("The processed SIH dataset is empty.")
        if len(self.df) != self.tfidf_matrix.shape[0]:
            raise ValueError(
                "Dataset rows and TF-IDF matrix rows do not match."
            )

    def recommend(self, user_input, top_n=10):
        valid, message = validate_user_query(user_input)
        if not valid:
            raise ValueError(message)

        try:
            top_n = int(top_n)
        except (TypeError, ValueError):
            top_n = 10
        top_n = max(1, min(top_n, len(self.df)))

        vector = self.vectorizer.transform([expand_user_query(user_input)])
        similarities = cosine_similarity(
            vector, self.tfidf_matrix
        ).flatten()

        relevant, _confidence = is_query_relevant(
            user_input, similarities
        )
        if not relevant:
            return []

        candidates = []
        for index in range(len(self.df)):
            problem = self.df.iloc[index]
            similarity = float(similarities[index])
            problem_text = safe_text(problem.get("weighted_text", ""))
            matched_skills = get_matched_skills(
                user_input, problem_text
            )
            theme_matches = get_theme_match(user_input, problem)

            candidates.append({
                "index": index,
                "similarity": similarity,
                "matched_skills": matched_skills,
                "theme_matches": theme_matches,
                "final_score": calculate_final_score(
                    user_input, problem, similarity
                ),
            })

        candidates = filter_relevant_candidates(candidates)
        candidates.sort(
            key=lambda item: (
                item["final_score"],
                item["similarity"],
                len(item["matched_skills"]),
            ),
            reverse=True,
        )

        results = []
        for rank, candidate in enumerate(candidates[:top_n], start=1):
            problem = self.df.iloc[candidate["index"]]
            results.append({
                "rank": rank,
                "ps_number": safe_text(problem.get("PS Number", "")),
                "title": safe_text(
                    problem.get("Problem Statement Title", "")
                ),
                "theme": safe_text(problem.get("Theme", "")),
                "category": safe_text(problem.get("Category", "")),
                "details": safe_text(problem.get("Details", "")),
                "tfidf_similarity": round(
                    candidate["similarity"] * 100, 2
                ),
                "final_score": round(
                    candidate["final_score"], 2
                ),
                "matched_skills": candidate["matched_skills"],
                "theme_matches": candidate["theme_matches"],
                "why_recommended": create_reason(
                    candidate["matched_skills"],
                    candidate["theme_matches"],
                ),
            })

        return results
