from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
import logging

from app.extensions import db
from app.models.tenant import Tenant
from app.models.users import User

business_bp = Blueprint("business", __name__, url_prefix="/api/business")
logger = logging.getLogger(__name__)


@business_bp.route("", methods=["POST"])
@jwt_required()
def create_business():
    """Create a new business/tenant."""
    try:
        user_id = get_jwt_identity()
        data = request.get_json(silent=True) or {}

        required_fields = ["business_name", "business_type", "phone", "email", "instance_name"]
        if not all(field in data for field in required_fields):
            return jsonify({"message": "Missing required fields"}), 400

        # Check if business already exists for this user
        existing = Tenant.query.filter_by(user_id=int(user_id)).first()
        if existing:
            return jsonify({"message": "User already has a business"}), 409

        business = Tenant(
            user_id=int(user_id),
            business_name=data.get("business_name"),
            business_type=data.get("business_type"),
            description=data.get("description", ""),
            phone=data.get("phone"),
            email=data.get("email"),
            instance_name=data.get("instance_name")
        )

        db.session.add(business)
        db.session.commit()

        logger.info(f"Business created: {business.id}")
        
        return jsonify({
            "message": "Business created successfully",
            "business": {
                "id": business.id,
                "business_name": business.business_name,
                "business_type": business.business_type,
                "description": business.description,
                "phone": business.phone,
                "email": business.email,
                "instance_name": business.instance_name
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating business: {str(e)}")
        return jsonify({"message": f"Failed to create business: {str(e)}"}), 500


@business_bp.route("", methods=["GET"])
@jwt_required()
def get_my_business():
    """Get current user's business."""
    try:
        user_id = get_jwt_identity()
        business = Tenant.query.filter_by(user_id=int(user_id)).first()

        if not business:
            return jsonify({"message": "No business found"}), 404

        return jsonify({
            "id": business.id,
            "business_name": business.business_name,
            "business_type": business.business_type,
            "description": business.description,
            "phone": business.phone,
            "email": business.email,
            "instance_name": business.instance_name,
            "created_at": business.created_at.isoformat()
        }), 200

    except Exception as e:
        logger.error(f"Error fetching business: {str(e)}")
        return jsonify({"message": f"Failed to fetch business: {str(e)}"}), 500


@business_bp.route("/<int:business_id>", methods=["PUT"])
@jwt_required()
def update_business(business_id):
    """Update business information."""
    try:
        user_id = get_jwt_identity()
        business = Tenant.query.filter_by(id=business_id, user_id=int(user_id)).first()

        if not business:
            return jsonify({"message": "Business not found"}), 404

        data = request.get_json(silent=True) or {}

        # Update allowed fields
        updatable_fields = ["business_name", "business_type", "description", "phone", "email", "instance_name"]
        for field in updatable_fields:
            if field in data:
                setattr(business, field, data[field])

        db.session.commit()
        logger.info(f"Business updated: {business_id}")

        return jsonify({
            "message": "Business updated successfully",
            "business": {
                "id": business.id,
                "business_name": business.business_name,
                "business_type": business.business_type,
                "description": business.description,
                "phone": business.phone,
                "email": business.email,
                "instance_name": business.instance_name
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating business: {str(e)}")
        return jsonify({"message": f"Failed to update business: {str(e)}"}), 500


@business_bp.route("/<int:business_id>", methods=["DELETE"])
@jwt_required()
def delete_business(business_id):
    """Delete business (soft delete by setting user_id to None)."""
    try:
        user_id = get_jwt_identity()
        business = Tenant.query.filter_by(id=business_id, user_id=int(user_id)).first()

        if not business:
            return jsonify({"message": "Business not found"}), 404

        db.session.delete(business)
        db.session.commit()
        logger.info(f"Business deleted: {business_id}")

        return jsonify({"message": "Business deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting business: {str(e)}")
        return jsonify({"message": f"Failed to delete business: {str(e)}"}), 500
