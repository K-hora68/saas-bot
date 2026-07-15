from app.extensions import db
from datetime import datetime

class Contact(db.Model):
    __tablename__ = "contacts"

    id = db.Column(db.Integer, primary_key = True)
    tenant_id = db.Column(db.Integer, db.ForeignKey("tenants.id"))
    phone = db.Column(db.String, nullable=False, unique = True)
    name = db.Column(db.String(20), nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default = datetime.utcnow)

    session_id = db.Column(db.Integer, db.ForeignKey("session.id"))

    tenants = db.relationship(
        "Tenant",
        back_populates = ("contacts")
    )