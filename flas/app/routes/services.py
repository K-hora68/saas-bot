from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

from app.extensions import db
from app.models.services import Service
from app.models.tenant import Tenant

services_bp = Blueprint("services", __name__, url_prefix="/api/services")
logger = logging.getLogger(__name__)


@services_bp.route("/", methods=["POST"])
@jwt_required()
def create_service():
    """Create a new service for the business."""
    try:
        user_id = get_jwt_identity()
        data = request.get_json(silent=True) or {}

        # Get user's business
        business = Tenant.query.filter_by(user_id=int(user_id)).first()
        if not business:
            return jsonify({"message": "Business not found"}), 404

        required_fields = ["name", "description", "price"]
        if not all(field in data for field in required_fields):
            return jsonify({"message": "Missing required fields"}), 400

        service = Service(
            tenant_id=business.id,
            name=data.get("name"),
            description=data.get("description"),
            price=data.get("price")
        )

        db.session.add(service)
        db.session.commit()

        logger.info(f"Service created: {service.id}")
        
        return jsonify({
            "message": "Service created successfully",
            "service": {
                "id": service.id,
                "name": service.name,
                "description": service.description,
                "price": service.price
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating service: {str(e)}")
        return jsonify({"message": f"Failed to create service: {str(e)}"}), 500


@services_bp.route("/", methods=["GET"])
@jwt_required()
def list_services():
    """Get all services for the business."""
    try:
        user_id = get_jwt_identity()
        business = Tenant.query.filter_by(user_id=int(user_id)).first()
        
        if not business:
            return jsonify({"message": "Business not found"}), 404

        services = Service.query.filter_by(tenant_id=business.id).all()
        
        return jsonify([{
            "id": s.id,
            "name": s.name,
            "description": s.description,
            "price": s.price,
            "created_at": s.created_at.isoformat() if s.created_at else None
        } for s in services]), 200

    except Exception as e:
        logger.error(f"Error fetching services: {str(e)}")
        return jsonify({"message": f"Failed to fetch services: {str(e)}"}), 500


@services_bp.route("/<int:service_id>", methods=["PUT"])
@jwt_required()
def update_service(service_id):
    """Update a service."""
    try:
        user_id = get_jwt_identity()
        business = Tenant.query.filter_by(user_id=int(user_id)).first()
        
        if not business:
            return jsonify({"message": "Business not found"}), 404

        service = Service.query.filter_by(id=service_id, tenant_id=business.id).first()
        if not service:
            return jsonify({"message": "Service not found"}), 404

        data = request.get_json(silent=True) or {}
        
        if "name" in data:
            service.name = data["name"]
        if "description" in data:
            service.description = data["description"]
        if "price" in data:
            service.price = data["price"]

        db.session.commit()
        logger.info(f"Service updated: {service_id}")

        return jsonify({
            "message": "Service updated successfully",
            "service": {
                "id": service.id,
                "name": service.name,
                "description": service.description,
                "price": service.price
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating service: {str(e)}")
        return jsonify({"message": f"Failed to update service: {str(e)}"}), 500


@services_bp.route("/<int:service_id>", methods=["DELETE"])
@jwt_required()
def delete_service(service_id):
    """Delete a service."""
    try:
        user_id = get_jwt_identity()
        business = Tenant.query.filter_by(user_id=int(user_id)).first()
        
        if not business:
            return jsonify({"message": "Business not found"}), 404

        service = Service.query.filter_by(id=service_id, tenant_id=business.id).first()
        if not service:
            return jsonify({"message": "Service not found"}), 404

        db.session.delete(service)
        db.session.commit()
        logger.info(f"Service deleted: {service_id}")

        return jsonify({"message": "Service deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting service: {str(e)}")
        return jsonify({"message": f"Failed to delete service: {str(e)}"}), 500
