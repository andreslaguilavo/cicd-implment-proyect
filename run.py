# run.py
from app import create_app

class LocalConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"  # archivo local
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True  # permite crear tablas automáticamente

def get_app():
    # Pasamos una configuración de prueba/local para forzar SQLite
    return create_app(test_config=LocalConfig)
