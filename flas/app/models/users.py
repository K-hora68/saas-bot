from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    tenant_id = db.Column(
        db.Integer,
        db.ForeignKey("tenants.id")
    )

    tenant = db.relationship(
        "Tenant",
        back_populates="users",
        foreign_keys=[tenant_id]
    )

    owned_tenants = db.relationship(
        "Tenant",
        back_populates="owner",
        foreign_keys="Tenant.owner_id",
        cascade="all, delete-orphan",
    )