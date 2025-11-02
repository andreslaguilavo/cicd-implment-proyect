import os
from flask import Flask, jsonify
from model.db import db

def _database_url_from_env():
    # Prefer DATABASE_URL, then SQLALCHEMY_DATABASE_URI, else default for docker-compose
    return (
        os.getenv("DATABASE_URL")
        or os.getenv("SQLALCHEMY_DATABASE_URI")
        or "mysql+mysqlconnector://appuser:apppass@db:3306/appdb"
    )

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = _database_url_from_env()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # init db
    db.init_app(app)

    # Import all models so SQLAlchemy maps tables
    from model.producto import Producto  # noqa: F401
    from model.cliente import Cliente    # noqa: F401
    from model.pedido import Pedido      # noqa: F401

    with app.app_context():
        db.create_all()

    # Register blueprints
    from controllers.producto import api as producto_api
    app.register_blueprint(producto_api, url_prefix="/api")

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    return app

# For gunicorn: app:create_app()
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
