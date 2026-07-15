from app.extensions import db
from datetime import datetime

class Service(db.model):
   __tablename__ = "services"

   id = db.Column(db.Interger, PrimaryKey = True)

   name = db.Comlumn(db.String(500), nullable = False)

   description = db.Column(db.string(500), nullable = False)
   price  = db.Column(db.String(40), nullable = False)
   
   user_id = db.Column(db.Interger, db.ForeignKey("users.id"))
   users = db.relationship("User", back_populates="services")

   tenant_id = db.Column(db.Integer, db.ForeignKey("tenants.id"))
   tenants = db.relationship(
      "Tenant",
      back_populates = "services"
   )

   created_at = db.Column(db.DateTime, default=datetime.utcnow)
   
