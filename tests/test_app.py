import importlib
import pytest

@pytest.fixture
def client(monkeypatch):
    app_module = importlib.import_module("app.app")
    app_module.app.config.update(TESTING=True, SECRET_KEY="test-secret")
    with app_module.app.test_client() as client:
        yield client

def _csrf_token(client):
    response = client.get("/")
    assert response.status_code == 200
    with client.session_transaction() as session:
        return session["csrf_token"]

def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"SIH AI" in response.data

def test_post_requires_csrf(client):
    response = client.post("/", data={"user_input": "Python Machine Learning"})
    assert response.status_code == 400

def test_empty_query_is_handled(client):
    token = _csrf_token(client)
    response = client.post("/", data={"csrf_token": token, "user_input": "   "})
    assert response.status_code == 200
    assert b"Please enter your skills and interests." in response.data

def test_security_headers(client):
    response = client.get("/")
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert "Content-Security-Policy" in response.headers
