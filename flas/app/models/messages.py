from datetime import datetime

from app.extensions import db


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    session_id = db.Column(
        db.Integer,
        db.ForeignKey("sessions.id"),
        nullable=False
    )

    sender = db.Column(
        db.String(20),
        nullable=False
    )
    # customer | bot

    message_type = db.Column(
        db.String(20),
        default="text",
        nullable=False
    )
    # text | image | document | audio | video

    content = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    sessions = db.relationship(
        "Session",
        back_populates="messages"
    )