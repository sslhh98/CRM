# modules/opportunities/models.py

from extensions import db
from datetime import datetime

class Opportunity(db.Model):
    __tablename__ = 'opportunities'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    amount      = db.Column(db.Float, nullable=True)
    close_date  = db.Column(db.Date, nullable=True)
    stage       = db.Column(db.String(50), nullable=False, default='Yeni')
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    # --- BUNLARI EKLE: ---
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    customer    = db.relationship(
        'Customer',
        back_populates='opportunities'
    )
