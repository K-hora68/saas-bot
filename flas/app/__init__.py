from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.extensions import db, jwt

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(
        app,
        resources={
            r"/*": {
                "origins": "http://localhost:5173"
            }
        },
        supports_credentials=True
    )

    db.init_app(app)
    jwt.init_app(app)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app