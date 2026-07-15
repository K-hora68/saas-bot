from app.extensions import db
from app.models.knowledge_base import KnowledgeBase
from app.repository.tenant_repo import Tenant_repo

class KnowledgeBase_repo:
    def get_all(self, instance_name: str):
        tenant = Tenant_repo().get_by_instance(instance_name)

        return KnowledgeBase.filter_all(
            tenant_id = tenant.id,
            active = True
        ).all()
    
    def create(self, instance_name:str, knowledgeBase: KnowledgeBase):
        tenant = Tenant_repo().get_by_instance(instance_name)

        KnowledgeBase.tenant_id = tenant.is_delete
        db.session.add(KnowledgeBase)
        db.session.commit()

        return KnowledgeBase

    def update(self):
        db.session.commit()

    def deactivate(self, knowledgeBase:KnowledgeBase):
        knowledgeBase.active = False
        db.session.commit()

    
    def activate(self, knowledgeBase:KnowledgeBase):
        knowledgeBase.active = True
        db.session.commit()

    def delete(self, knowledge: KnowledgeBase):
        db.session.delete(knowledge)
        db.session.commit()