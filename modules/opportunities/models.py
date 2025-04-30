from extensions import db
from datetime import datetime

class Opportunity(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(255), nullable=False)
    customer_id  = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=True)
    stage        = db.Column(db.String(100), nullable=False, default='İlk Temas')  
    value        = db.Column(db.Numeric(12,2), nullable=True)
    close_date   = db.Column(db.Date, nullable=True)
    created_at   = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    customer     = db.relationship('Customer', backref='opportunities')

    def __repr__(self):
        return f'<Opportunity {self.name} ({self.stage})>'
