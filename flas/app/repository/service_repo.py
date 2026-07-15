from app.models.services import Service
from app.extensions import db
from app.repository.tenant_repo import Tenant_repo

class Service_repo:
    def get_all(self, instance_name: str):
        tenant = Tenant_repo().get_by_instance(instance_name)

        return Service.query.filter_by(
           tenant_id = tenant.id,
           active = True
        ).all()
    
    def get_by_id(self, service_id:int):
        return Service.query.get(service_id)
    
    def create(self, instance_name:str, service: Service):
        tenant = Tenant_repo().get_by_instance(instance_name)

        service.tenant_id = tenant.id 

        db.session.add(service)
        db.session.commit()

    def update(self):
            db.session.commit()
        
    def activate(self, service: Service):
         service.active = False
         db.session.commit()

    def delete(self, service: Service):
         db.session.delete(service)
         db.session.commit()
        