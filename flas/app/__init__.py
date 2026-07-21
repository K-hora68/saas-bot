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

    # Import all models
    importlib.import_module("app.models.users")
    importlib.import_module("app.models.tenant")
    importlib.import_module("app.models.contacts")
    importlib.import_module("app.models.session")
    importlib.import_module("app.models.messages")
    importlib.import_module("app.models.services")
    importlib.import_module("app.models.knowledge_base")
    importlib.import_module("app.models.flows")

    from app.routes.auth import auth_bp
    from app.routes.webhook import webhook_bp
    from app.routes.business import business_bp
    from app.routes.services import services_bp
    from app.routes.knowledge import knowledge_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(webhook_bp)
    app.register_blueprint(business_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(knowledge_bp)

    return app