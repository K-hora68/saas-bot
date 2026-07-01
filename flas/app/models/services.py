from app import db

class Service(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    name = db.Column(db.String(255), nullable=False)

    description = db.Column(db.String(255))

    price = db.Column(db.Float)

    image_url = db.Column(db.String(555))

    business_id = db.Column(
        db.Interger,
        ForeignKey = True,
        nullable = False
    )
    tenant = db.relationship("Tenants", back_populates = "Service")