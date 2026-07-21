from app.extensions import db
from app.models.contacts import Contact
from app.repository.tenant_repo import Tenant_repo

class Contact_repo:
    def get_by_phone(
            self,
            instance_name:str,
            phone: str,
            name
    ):
        tenant = Tenant_repo().get_by_instance(instance_name)
        return Contact.query.filter_by(
            tenant_id = tenant.id,
            phone = phone
        ).first()
    
    def create(
            self,
            instance_name: str,
            phone: str,
            name:str=None
    ):
        tenant = Tenant_repo().get_by_instance(instance_name)
        contact = Contact(
            tenant_id = tenant.id,
            name = name,
            phone = phone
        )
        db.session.add(contact)
        db.session.commit()

        return contact
    
    def get_or_create(
        self,
        instance_name: str,
        phone: str,
        name: str = None
    ):
       tenant = Tenant_repo().get_by_instance(instance_name)

       if tenant is None:
        return None

    # Remove the WhatsApp suffix if present
       phone = phone.split("@")[0]

       contact = Contact.query.filter_by(
         tenant_id=tenant.id,
         phone=phone
       ).first()

       if contact:
        return contact

       return self.create(
        instance_name=instance_name,
        phone=phone,
        name=name
    )
    def update(self):
        db.session.commit()

    def delete(self, contact: Contact):
        db.session.delete(contact)
        db.session.commit()
