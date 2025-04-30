from extensions import db

class Customer(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    name    = db.Column(db.String(128), nullable=False)
    phone   = db.Column(db.String(32), nullable=False)
    email   = db.Column(db.String(128), nullable=False)
    status  = db.Column(db.String(64), nullable=False)
    tag     = db.Column(db.String(64), unique=True, nullable=False)  # <-- Yeni alan

    def __repr__(self):
        return f'<Customer {self.name} #{self.tag}>'
