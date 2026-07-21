from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.models.services import Service
from app.models.tenant import Tenant
from app.models.users import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.get_json(silent=True) or {}

        if not data.get("username") or not data.get("email") or not data.get("password"):
            return jsonify({"message": "Missing required fields"}), 400

        user = User(
            username=data["username"],
            email=data["email"],
            password=generate_password_hash(data["password"]),
        )

        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as exc:
        db.session.rollback()
        return jsonify({"message": f"Registration failed: {str(exc)}"}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json(silent=True) or {}

        if not data.get("email") or not data.get("password"):
            return jsonify({"message": "Missing email or password"}), 400

        user = User.query.filter_by(email=data["email"]).first()
        if not user:
            return jsonify({"message": "Invalid email or password"}), 401
        if not check_password_hash(user.password, data["password"]):
            return jsonify({"message": "Invalid email or password"}), 401

        token = create_access_token(identity=str(user.id))

        return jsonify(
            {
                "access_token": token,
                "user_id": user.id,
                "username": user.username,
            }
        ), 200
    except Exception as exc:
        return jsonify({"message": f"Login failed: {str(exc)}"}), 500


@auth_bp.route("/is_authenticated", methods=["GET"])
@jwt_required()
def is_authenticated():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    if user:
        return jsonify({"authenticated": True, "user_id": user.id}), 200
    return jsonify({"authenticated": False}), 401


@auth_bp.route("/api/services", methods=["POST"])
@jwt_required()
def create_service():
    try:
        user_id = int(get_jwt_identity())
        services_data = request.get_json(silent=True) or []

        if not isinstance(services_data, list):
            return jsonify({"message": "Services must be a list"}), 400
        
        tenant = Tenant.query.filter_by(user_id=user_id).first()
        if not tenant:
            return jsonify({"message": "Business not found"})
      
        for service_data in services_data:
            if not service_data.get("name"):
                return jsonify({"message": "Service name is required"}), 400
            new_service = Service(
                user_id=user_id,
                name=service_data.get("name"),
                description=service_data.get("description"),
                price=service_data.get("price"),
                tenant_id=tenant.id
            )
            db.session.add(new_service)
        db.session.commit()

        return jsonify({"message": "saved"}), 201
    except Exception as exc:
        db.session.rollback()
        return jsonify({"message": f"Failed to save services: {str(exc)}"}), 500
    