from app.extensions import db
from datetime import datetime

class Tenant(db.Model):
    
    __tablename__ = "tenants"

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    business_name = db.Column(db.String(20),nullable = False)

    business_type = db.Column(db.String(22), nullable = False)

    description = db.Column(db.String(500), nullable = True)
     
    phone = db.Column(db.String(15), unique = True, nullable = False)

    email = db.Column(db.String(15), unique = True, nullable = False)

    instance_name = db.Column(db.String(20), nullable = False)

    created_at = db.Column(db.DateTime, default = datetime.utcnow)

    contacts = db.relationship(
        "Contact",
        back_populates = "tenants"
    )

    services = db.relationship(
        "Service",
        back_populates = "tenants"
    )
