import os
import pytest
from dotenv import load_dotenv
import sys
from pathlib import Path
# Ensure repo root is on sys.path so packages like 'model' can be imported
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from model.db import db
from app import create_app


load_dotenv()  # ensure .env variables are loaded


@pytest.fixture(scope="session", autouse=True)
def env_vars():
    # Force the test DB and testing mode (use sqlite and testing True)
    os.environ["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///app.db")
    os.environ["TESTING"] = os.getenv("TESTING", "true")
    yield
    # optional session cleanup: remove sqlite DB file if created
    db_path = os.environ.get("SQLALCHEMY_DATABASE_URI",
                             "sqlite:///app.db").replace("sqlite:///", "")
    if db_path and os.path.exists(db_path):
        try:
            os.remove(db_path)
        except Exception:
            pass


@pytest.fixture
def client():
    # Create app and test client, ensure db is initialized and cleaned after each test
    app = create_app()
    app.testing = os.environ.get("TESTING", "true").lower() == "true"

    with app.app_context():
        db.create_all()
        client = app.test_client()

        yield client

        # Teardown: close session and drop tables to avoid ResourceWarnings
        db.session.remove()
        db.drop_all()

    # Optionally remove SQLite file each test run (keeps isolation)
    db_path = os.environ.get("SQLALCHEMY_DATABASE_URI",
                             "sqlite:///app.db").replace("sqlite:///", "")
    if db_path and os.path.exists(db_path):
        try:
            os.remove(db_path)
        except Exception:
            pass
