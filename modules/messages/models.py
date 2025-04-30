from extensions import db
from datetime import datetime

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    tag = db.Column(db.String(50))  # Etiket (isteğe bağlı)

    def __repr__(self):
        return f'<Message {self.id}>'
