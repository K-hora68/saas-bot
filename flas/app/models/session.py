from app.extensions import db
from datetime import datetime

class Session(db.Model):
    __tablename__ = "sessions"
    id = db.Column(db.Integer, primary_key= True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.id"), nullable = False)
    current_step = db.Column(db.Interger, db.ForeignKey("services.id"))
   
    status = db.Column(db.Boolean, default=False)

    created_at= db.Column(db.DateTime, default = datetime.utcnow)
    updated_at = db.Column(db.DateTime, defaulta= datetime.utcnow, onupdate=datetime.utcnow)