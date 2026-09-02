"""
Main SIH AI Recommendation Engine.
"""


import pickle

import numpy as np

import pandas as pd

from sklearn.metrics.pairwise import (
    cosine_similarity
)


from .skill_matching import (
    get_matched_skills
)


from .scoring import (
    get_theme_match,
    calculate_final_score
)


from .utils import (
    validate_user_input,
    create_reason
)


class SIHRecommender:

    """
    SIH AI Problem Recommendation System.
    """


    def __init__(
        self,
        vectorizer_path,
        matrix_path,
        dataset_path
    ):

        # Load TF-IDF vectorizer
        with open(
            vectorizer_path,
            "rb"
        ) as file:

            self.vectorizer = (
                pickle.load(file)
            )


        # Load TF-IDF matrix
        with open(
            matrix_path,
            "rb"
        ) as file:

            self.tfidf_matrix = (
                pickle.load(file)
            )


        # Load processed dataset
        self.df = pd.read_csv(
            dataset_path
        )


        # Safety check
        if (
            len(self.df)
            !=
            self.tfidf_matrix.shape[0]
        ):

            raise ValueError(
                "Dataset rows and TF-IDF "
                "matrix rows do not match."
            )


    def recommend(
        self,
        user_input,
        top_n=10
    ):

        """
        Generate Top N SIH recommendations.
        """

        # Validate input
        if not validate_user_input(
            user_input
        ):

            raise ValueError(
                "Please enter at least one "
                "skill or interest."
            )


        # Prevent invalid Top N
        top_n = max(
            1,
            min(
                int(top_n),
                len(self.df)
            )
        )


        # Convert user input
        # into TF-IDF vector
        user_vector = (
            self.vectorizer.transform(
                [str(user_input)]
            )
        )


        # Calculate cosine similarity
        similarity_scores = (
            cosine_similarity(
                user_vector,
                self.tfidf_matrix
            )
            .flatten()
        )


        # Calculate final hybrid scores
        final_scores = []


        for index in range(
            len(self.df)
        ):

            problem = (
                self.df.iloc[index]
            )


            score = (
                calculate_final_score(
                    user_input,
                    problem,
                    similarity_scores[index]
                )
            )


            final_scores.append(
                score
            )


        # Convert to NumPy array
        final_scores = np.array(
            final_scores
        )


        # Get Top N indices
        top_indices = (
            final_scores
            .argsort()[-top_n:]
            [::-1]
        )


        # Create final results
        results = []


        for rank, index in enumerate(
            top_indices,
            start=1
        ):

            problem = (
                self.df.iloc[index]
            )


            # Find skill matches
            matched_skills = (
                get_matched_skills(
                    user_input,
                    problem.get(
                        "weighted_text",
                        ""
                    )
                )
            )


            # Find theme matches
            theme_matches = (
                get_theme_match(
                    user_input,
                    problem
                )
            )


            # Generate explanation
            reason = (
                create_reason(
                    matched_skills,
                    theme_matches
                )
            )


            result = {

                "rank":
                rank,


                "ps_number":
                problem.get(
                    "PS Number",
                    ""
                ),


                "title":
                problem.get(
                    "Problem Statement Title",
                    ""
                ),


                "theme":
                problem.get(
                    "Theme",
                    ""
                ),


                "category":
                problem.get(
                    "Category",
                    ""
                ),


                "details":
                problem.get(
                    "Details",
                    ""
                ),


                "tfidf_similarity":
                round(
                    float(
                        similarity_scores[index]
                    )
                    * 100,
                    2
                ),


                "final_score":
                round(
                    float(
                        final_scores[index]
                    ),
                    2
                ),


                "matched_skills":
                matched_skills,


                "theme_matches":
                theme_matches,


                "why_recommended":
                reason
            }


            results.append(
                result
            )


        return results