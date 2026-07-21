from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

from app.extensions import db
from app.models.knowledge_base import KnowledgeBase
from app.models.tenant import Tenant

knowledge_bp = Blueprint("knowledge", __name__, url_prefix="/api/knowledge")
logger = logging.getLogger(__name__)


@knowledge_bp.route("/", methods=["POST"])
@jwt_required()
def create_knowledge():
    """Create a new knowledge base entry."""
    try:
        user_id = get_jwt_identity()
        data = request.get_json(silent=True) or {}

        # Get user's business
        business = Tenant.query.filter_by(user_id=int(user_id)).first()
        if not business:
            return jsonify({"message": "Business not found"}), 404

        required_fields = ["title", "content"]
        if not all(field in data for field in required_fields):
            return jsonify({"message": "Missing required fields"}), 400

        knowledge = KnowledgeBase(
            tenant_id=business.id,
            title=data.get("title"),
            content=data.get("content")
        )

        db.session.add(knowledge)
        db.session.commit()

        logger.info(f"Knowledge entry created: {knowledge.id}")
        
        return jsonify({
            "message": "Knowledge entry created successfully",
            "knowledge": {
                "id": knowledge.id,
                "title": knowledge.title,
                "content": knowledge.content
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating knowledge entry: {str(e)}")
        return jsonify({"message": f"Failed to create knowledge entry: {str(e)}"}), 500


@knowledge_bp.route("/", methods=["GET"])
@jwt_required()
def list_knowledge():
    """Get all knowledge base entries for the business."""
    try:
        user_id = get_jwt_identity()
        business = Tenant.query.filter_by(user_id=int(user_id)).first()
        
        if not business:
            return jsonify({"message": "Business not found"}), 404

        entries = KnowledgeBase.query.filter_by(tenant_id=business.id).all()
        
        return jsonify([{
            "id": e.id,
            "title": e.title,
            "question": e.question,  # Property alias
            "content": e.content,
            "answer": e.answer,      # Property alias
            "created_at": e.created_at.isoformat() if e.created_at else None
        } for e in entries]), 200

    except Exception as e:
        logger.error(f"Error fetching knowledge entries: {str(e)}")
        return jsonify({"message": f"Failed to fetch knowledge entries: {str(e)}"}), 500


@knowledge_bp.route("/<int:knowledge_id>", methods=["PUT"])
@jwt_required()
def update_knowledge(knowledge_id):
    """Update a knowledge base entry."""
    try:
        user_id = get_jwt_identity()
        business = Tenant.query.filter_by(user_id=int(user_id)).first()
        
        if not business:
            return jsonify({"message": "Business not found"}), 404

        knowledge = KnowledgeBase.query.filter_by(id=knowledge_id, tenant_id=business.id).first()
        if not knowledge:
            return jsonify({"message": "Knowledge entry not found"}), 404

        data = request.get_json(silent=True) or {}
        
        if "title" in data:
            knowledge.title = data["title"]
        if "content" in data:
            knowledge.content = data["content"]

        db.session.commit()
        logger.info(f"Knowledge entry updated: {knowledge_id}")

        return jsonify({
            "message": "Knowledge entry updated successfully",
            "knowledge": {
                "id": knowledge.id,
                "title": knowledge.title,
                "content": knowledge.content
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating knowledge entry: {str(e)}")
        return jsonify({"message": f"Failed to update knowledge entry: {str(e)}"}), 500


@knowledge_bp.route("/<int:knowledge_id>", methods=["DELETE"])
@jwt_required()
def delete_knowledge(knowledge_id):
    """Delete a knowledge base entry."""
    try:
        user_id = get_jwt_identity()
        business = Tenant.query.filter_by(user_id=int(user_id)).first()
        
        if not business:
            return jsonify({"message": "Business not found"}), 404

        knowledge = KnowledgeBase.query.filter_by(id=knowledge_id, tenant_id=business.id).first()
        if not knowledge:
            return jsonify({"message": "Knowledge entry not found"}), 404

        db.session.delete(knowledge)
        db.session.commit()
        logger.info(f"Knowledge entry deleted: {knowledge_id}")

        return jsonify({"message": "Knowledge entry deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting knowledge entry: {str(e)}")
        return jsonify({"message": f"Failed to delete knowledge entry: {str(e)}"}), 500
