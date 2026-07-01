from datetime import datetime
from app import db

class Conversation(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True)

    user_phone = db.Column(db.String(16), nullable = False, index = True)

    tenant_id = db.Column(
        db.Integer,
        db.ForeignKey("tenants.id"),
        nullable=False,
        index=True
    )
    tenant = db.relationship("Tenants")

    context_state = db.Column(db.JSON, default = dict)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    messages = db.relationship("Message", back_populates = "Conversation")

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime,
        default = datetime.utcnow
    )