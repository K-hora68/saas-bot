from app.models.tenant import Tenant
from app.extensions import db

class Tenant_repo:
    def get_by_id(self, tenant_id):
        return Tenant.query.get(tenant_id)
    
    def get_by_instance(self, instance_name: str):
        return Tenant.query.filter_by(instance_name=instance_name)
    
    def get_all(self):
        return Tenant.query.all()
    
    def create(self, tenant: Tenant):
        db.session.add(tenant)
        db.session.commit()
        return tenant
    
    def update(self):
        db.session.commit()
    
    def delete(self, tenant: Tenant):
        db.session.delete(tenant)
        db.session.commit()

    def get_by_owner(self, owner_id: int):
        return Tenant.query.filter_by(id = owner_id).first()
    
    def exists(self, tenant_id: int,instance_name: str):
        return Tenant.query.filter_by(id = tenant_id, instance_name = instance_name).first
    