import sys
import time
from collections import defaultdict, deque
from pathlib import Path

from flask import Flask, abort, render_template, request
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.middleware.proxy_fix import ProxyFix

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.config import (
    DATASET_PATH,
    DEBUG,
    HOST,
    MATRIX_PATH,
    MAX_CONTENT_LENGTH,
    PORT,
    SECRET_KEY,
    SESSION_COOKIE_HTTPONLY,
    SESSION_COOKIE_SAMESITE,
    SESSION_COOKIE_SECURE,
    VECTOR_PATH,
)
from src.recommender import SIHRecommender

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

app.config.update(
    SECRET_KEY=SECRET_KEY,
    MAX_CONTENT_LENGTH=MAX_CONTENT_LENGTH,
    SESSION_COOKIE_HTTPONLY=SESSION_COOKIE_HTTPONLY,
    SESSION_COOKIE_SAMESITE=SESSION_COOKIE_SAMESITE,
    SESSION_COOKIE_SECURE=SESSION_COOKIE_SECURE,
)

recommender = SIHRecommender(
    vectorizer_path=VECTOR_PATH,
    matrix_path=MATRIX_PATH,
    dataset_path=DATASET_PATH,
)

RATE_LIMIT = 30
RATE_WINDOW_SECONDS = 60
_request_log = defaultdict(deque)


def client_key():
    forwarded = request.headers.get("X-Forwarded-For", "")
    return forwarded.split(",")[0].strip() or request.remote_addr or "unknown"


def rate_limit_ok():
    now = time.time()
    key = client_key()
    bucket = _request_log[key]
    while bucket and now - bucket[0] > RATE_WINDOW_SECONDS:
        bucket.popleft()
    if len(bucket) >= RATE_LIMIT:
        return False
    bucket.append(now)
    return True



@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self'; "
        "img-src 'self' data:; "
        "font-src 'self'; "
        "connect-src 'self'; "
        "base-uri 'self'; "
        "form-action 'self'; "
        "frame-ancestors 'none'"
    )
    if request.is_secure or request.headers.get("X-Forwarded-Proto") == "https":
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
    return response


@app.errorhandler(RequestEntityTooLarge)
def handle_large_request(_error):
    return render_template(
        "index.html",
        results=[],
        user_input="",
        error="Input is too large. Please enter a shorter query.",
    ), 413


@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    user_input = ""
    error = None
    info = None

    if request.method == "POST":
        if not rate_limit_ok():
            abort(429)


        user_input = request.form.get("user_input", "").strip()

        if len(user_input) > 500:
            error = "Please keep your skills and interests under 500 characters."
        elif not user_input:
            error = "Please enter your skills and interests."
        else:
            try:
                results = recommender.recommend(user_input, top_n=10)
                if not results:
                    info = (
                        "No confident SIH problem match was found. "
                        "Try entering skills, technologies, or domains such as "
                        "Python, Machine Learning, Computer Vision, Robotics, "
                        "Agriculture, or Cybersecurity."
                    )
            except ValueError as exc:
                error = str(exc)
            except Exception:
                app.logger.exception("Recommendation request failed")
                error = (
                    "The recommendation service is temporarily unavailable. "
                    "Please try again."
                )

    return render_template(
        "index.html",
        results=results,
        user_input=user_input,
        error=error,
        info=info,
    )


@app.errorhandler(400)
def bad_request(_error):
    return render_template(
        "index.html",
        results=[],
        user_input="",
        error="Invalid or expired request. Please refresh the page and try again.",
    ), 400


@app.errorhandler(429)
def too_many_requests(_error):
    return render_template(
        "index.html",
        results=[],
        user_input="",
        error="Too many requests. Please wait a moment and try again.",
    ), 429


if __name__ == "__main__":
    app.run(debug=DEBUG, host=HOST, port=PORT)
