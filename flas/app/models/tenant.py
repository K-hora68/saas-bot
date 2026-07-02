from datetime import datetime
from app.extensions import db


class Tenant(db.Model):
    __tablename__ = "tenants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    business_type = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(120))

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    owner = db.relationship(
        "User",
        back_populates="owned_tenants",
        foreign_keys=[owner_id]
    )

    users = db.relationship(
        "User",
        back_populates="tenant",
        foreign_keys="User.tenant_id",
        cascade="all, delete-orphan"
    )

    services = db.relationship(
        "Service",
        back_populates="tenant",
        cascade="all, delete"
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)