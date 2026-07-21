from app.extensions import db
from datetime import datetime

class KnowledgeBase(db.Model):
    __tablename__ = "knowledges"

    id = db.Column(db.Integer, primary_key = True)
    tenant_id = db.Column(db.Integer, db.ForeignKey("tenants.id"))
    
    title = db.Column(db.String(50), nullable = False)
    content = db.Column(db.String(500), nullable=False)
    
    # Aliases for compatibility with prompt builder
    @property
    def question(self):
        return self.title
    
    @property
    def answer(self):
        return self.content

    created_at = db.Column(db.DateTime, default=datetime.utcnow)