# modules/customers/models.py

from extensions import db

class Customer(db.Model):
    __tablename__ = 'customers'
    id     = db.Column(db.Integer, primary_key=True)
    name   = db.Column(db.String(100), nullable=False)
    email  = db.Column(db.String(120), unique=True, nullable=False)
    phone  = db.Column(db.String(30), nullable=True)
    # …

    # --- BUNU EKLE: ---
    opportunities = db.relationship(
        'Opportunity',
        back_populates='customer',
        cascade='all, delete-orphan'
    )
