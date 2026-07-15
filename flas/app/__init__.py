import importlib

from flask import Flask
from flask_cors import CORS
from datetime import timedelta

from app.config import Config
from app.extensions import db, jwt


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

    CORS(
        app,
        resources={r"/*": {"origins": "http://localhost:5173"}},
        supports_credentials=True,
    )

    db.init_app(app)
    jwt.init_app(app)

    importlib.import_module("app.models.customers")
    importlib.import_module("app.models.conversations")
    importlib.import_module("app.models.messages")
    importlib.import_module("app.models.services")
    importlib.import_module("app.models.tenant")
    importlib.import_module("app.models.users")
    importlib.import_module("app.models.flows")
    importlib.import_module("app.models.questions")
    importlib.import_module("app.models.options")
    importlib.import_module("app.models.responses")
    importlib.import_module("app.models.response_options")
    importlib.import_module("app.models.tags")

    from app.routes.auth import auth_bp

    app.register_blueprint(auth_bp)

    return app