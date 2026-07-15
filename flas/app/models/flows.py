from app.extensions import db
from datetime import datetime

class Flow(db.Model):
    __tablename__ = "flows"

    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey("tenants.id"))
    created_at = db.Column(db.DateTime, default = datetime.utc.now)
