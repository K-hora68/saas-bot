from app import db
from datetime import datetime

class Tenant(db.Model):
    __tablename__ = "tenants"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)

    business_type = db.Column(db.String(120))  # salon, car dealer, clinic

    phone = db.Column(db.String(50))

    email = db.Column(db.String(120))

    owner_id = db.Column(
        db.Interger,
        ForeignKey = ("users.id"),
        nullable = False
        )
    owner = db.relationship("User", back_populates = "tenants")
    services = db.relationship("Service", back_populates="tenants", cascade="all, delete")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)