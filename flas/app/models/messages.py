from app.extensions import db
from datetime import datetime

class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)

    tenant_id = db.Column(
        db.Integer,
        db.ForeignKey("tenants.id"),
        nullable=False
    )

    contact_id = db.Column(
        db.Integer,
        db.ForeignKey("contacts.id"),
        nullable=False
    )

    direction = db.Column(db.String(10), nullable=False)
    message = db.Column(db.Text, nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )