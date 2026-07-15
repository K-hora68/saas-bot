from app.extensions import db
from datetime import datetime

class KnowledgeBase(db.Model):
    __tablename__ = "knowledges"

    id = db.Column(db.Integer, primary_key = True)
    tenant_id = db.Column(db.Integer, db.ForeignKey("knowlegdes.id"))
    
    title = db.Column(db.String(50), nullable = False)
    content = db.Column(db.String(500, nullable=False))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)