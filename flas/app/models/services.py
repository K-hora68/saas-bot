from app.extensions import db
from datetime import datetime

class Service(db.Model):
   __tablename__ = "services"

   id = db.Column(db.Integer, primary_key = True)

   name = db.Column(db.String(500), nullable = False)

   description = db.Column(db.String(500), nullable = False)
   price  = db.Column(db.String(40), nullable = False)
   
   user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
   users = db.relationship("User", back_populates="services")

   tenant_id = db.Column(db.Integer, db.ForeignKey("tenants.id"))
   tenants = db.relationship(
      "Tenant",
      back_populates = "services"
   )
   active = db.Column(db.Boolean, default=True)
   created_at = db.Column(db.DateTime, default=datetime.utcnow)
   
