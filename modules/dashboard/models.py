from datetime import datetime
from extensions import db

class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    # İster kullanıcı modeliniz varsa ForeignKey('user.id') ekleyin, yoksa numeric olarak saklayın
    user_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=True)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # İlişkiler
    # Eğer bir User modeli mevcutsa aşağıdaki satırı aktif edin ve doğru yolu belirtin
    # user = db.relationship('User', backref='activities')
    customer = db.relationship('Customer', backref='activities')
