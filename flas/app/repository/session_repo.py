# from app.extensions import db
# from app.models.session import Session
# from app.repository.tenant_repo import Tenant_repo

from app.extensions import db
from app.models.session import Session


class Session_repo:

    def get_active(
        self,
        contact_id: int,
    ):
        return Session.query.filter_by(
            contact_id=contact_id,
            status=True
        ).first()

    def create(
        self,
        contact_id: int
    ):
        session = Session(
            contact_id=contact_id,
            status=True
        )

        db.session.add(session)
        db.session.commit()

        return session

    def get_or_create(
        self,
        contact_id: int
    ):
        session = self.get_active(contact_id)

        if session:
            return session

        return self.create(contact_id)

    def update(self):
        db.session.commit()

    def close(self, session: Session):
        session.status = False
        db.session.commit()

    def delete(self, session: Session):
        db.session.delete(session)
        db.session.commit()