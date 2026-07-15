from app.extensions import db
from models.session import Session
from repository.tenant_repo import Tenant_repo

class Session_repo:

    def get_active(
            self,
            contact_id: int,
            instance_name: str,
            status
    ):
        tenant = Tenant_repo().get_by_instance(instance_name)
        return Session.query.filter_by(contact_id = contact_id, instance_name = instance_name, status = True).first()
    
    def create(
            self,
            instance_name: str,
            contact_id: int
    ):
        tenant = Tenant_repo().get_by_instance(instance_name)

        session = Session(
            tenant_id = tenant.id,
            instance_name = instance_name,
            contact_id = contact_id,
            status = True
       )
        
        db.session.add(session)
        db.session.commit()

        return session
    
    def get_or_create(
            self,
            contact_id:int,
            instance_name: int,
    ):
        session = self.get_active(
        instance_name,
        contact_id
        ) 

        if session:
            return session
        
        return self.create(
            instance_name,
            contact_id
        )

    def update(self):
        db.session.commit()

    def close(self, session: Session):
        session.status = False
        db.session.commit()

    def delete(self, session: Session):
        db.session.delete(session)
        db.session.commit()