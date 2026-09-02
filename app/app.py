# Application entry point
from flask import (
    Flask,
    render_template,
    request
)

from app.config import (
    VECTOR_PATH,
    MATRIX_PATH,
    DATASET_PATH,
    DEBUG,
    HOST,
    PORT
)

import sys
from pathlib import Path


# Add project root to Python path
PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

sys.path.append(
    str(PROJECT_ROOT)
)


from src.recommender import (
    SIHRecommender
)


app = Flask(__name__)


# Load AI recommendation system
recommender = SIHRecommender(

    vectorizer_path=VECTOR_PATH,

    matrix_path=MATRIX_PATH,

    dataset_path=DATASET_PATH
)


@app.route(
    "/",
    methods=["GET", "POST"]
)
def index():

    results = []

    user_input = ""

    error = None


    if request.method == "POST":

        user_input = (
            request.form
            .get(
                "user_input",
                ""
            )
            .strip()
        )


        if not user_input:

            error = (
                "Please enter your skills "
                "and interests."
            )


        else:

            try:

                results = (
                    recommender.recommend(
                        user_input,
                        top_n=10
                    )
                )


            except Exception as e:

                error = str(e)


    return render_template(

        "index.html",

        results=results,

        user_input=user_input,

        error=error
    )


if __name__ == "__main__":

    app.run(

        debug=DEBUG,

        host=HOST,

        port=PORT
    )