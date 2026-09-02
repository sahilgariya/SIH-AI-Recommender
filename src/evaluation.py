"""
Recommendation evaluation functions.
"""


import numpy as np

import pandas as pd

from sklearn.metrics.pairwise import (
    cosine_similarity
)


from .skill_matching import (
    get_matched_skills
)


from .scoring import (
    calculate_final_score
)


def evaluate_recommendation(
    user_input,
    vectorizer,
    tfidf_matrix,
    df,
    top_n=10
):

    """
    Evaluate the Top N recommendations.
    """


    # Convert user input
    user_vector = (
        vectorizer.transform(
            [str(user_input)]
        )
    )


    # Calculate similarity
    similarity_scores = (
        cosine_similarity(
            user_vector,
            tfidf_matrix
        )
        .flatten()
    )


    # Calculate final scores
    final_scores = []


    for index in range(
        len(df)
    ):

        score = (
            calculate_final_score(
                user_input,
                df.iloc[index],
                similarity_scores[index]
            )
        )

        final_scores.append(
            score
        )


    final_scores = np.array(
        final_scores
    )


    # Get Top N results
    top_indices = (
        final_scores
        .argsort()[-top_n:]
        [::-1]
    )


    evaluation_results = []


    for rank, index in enumerate(
        top_indices,
        start=1
    ):

        problem = (
            df.iloc[index]
        )


        matched_skills = (
            get_matched_skills(
                user_input,
                problem.get(
                    "weighted_text",
                    ""
                )
            )
        )


        evaluation_results.append({

            "Rank":
            rank,


            "PS Number":
            problem.get(
                "PS Number",
                ""
            ),


            "Title":
            problem.get(
                "Problem Statement Title",
                ""
            ),


            "Matched Skills":
            ", ".join(
                matched_skills
            ),


            "Number of Matches":
            len(
                matched_skills
            ),


            "Final Score":
            round(
                float(
                    final_scores[index]
                ),
                2
            )
        })


    evaluation_df = (
        pd.DataFrame(
            evaluation_results
        )
    )


    return evaluation_df