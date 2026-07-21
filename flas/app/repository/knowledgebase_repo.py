from app.extensions import db
from app.models.knowledge_base import KnowledgeBase
from app.repository.tenant_repo import Tenant_repo


class KnowledgeBase_repo:

    def get_all(self, instance_name: str):
        tenant = Tenant_repo().get_by_instance(instance_name)

        if tenant is None:
            return []

        return KnowledgeBase.query.filter_by(
            tenant_id=tenant.id
        ).all()

    def create(self, instance_name: str, knowledgeBase: KnowledgeBase):
        tenant = Tenant_repo().get_by_instance(instance_name)

        if tenant is None:
            return None

        knowledgeBase.tenant_id = tenant.id

        db.session.add(knowledgeBase)
        db.session.commit()

        return knowledgeBase

    def update(self):
        db.session.commit()

    def deactivate(self, knowledgeBase: KnowledgeBase):
        knowledgeBase.active = False
        db.session.commit()

    def activate(self, knowledgeBase: KnowledgeBase):
        knowledgeBase.active = True
        db.session.commit()

    def delete(self, knowledgeBase: KnowledgeBase):
        db.session.delete(knowledgeBase)
        db.session.commit()