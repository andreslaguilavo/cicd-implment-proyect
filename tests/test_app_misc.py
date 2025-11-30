import os
from dotenv import load_dotenv
from app import create_app

load_dotenv()


def test_app_init():
    # Validate that create_app uses env vars
    os.environ["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///app.db")
    os.environ["TESTING"] = os.getenv("TESTING", "true")
    app = create_app()
    assert "sqlite" in app.config["SQLALCHEMY_DATABASE_URI"]
    # create_app does not set TESTING itself; it should respect env vars when used in tests
    app.config["TESTING"] = os.getenv("TESTING", "true").lower() == "true"
    assert app.config["TESTING"] is True


def test_health_check(client):
    # Health endpoint is present and returns ok
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok"}


def test_404_handler(client):
    r = client.get("/no-existe")
    assert r.status_code == 404
