import os
from app import create_app
from dotenv import load_dotenv

load_dotenv()


def test_health_check():
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///app.db")
    app.config["TESTING"] = os.getenv("TESTING", "true").lower() == "true"
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json().get("status") == "ok"
