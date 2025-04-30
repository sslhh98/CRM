from extensions import db
from datetime import datetime

class Task(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status      = db.Column(db.String(50), nullable=False, default='Beklemede')  # Beklemede, Devam, Tamamlandı
    due_date    = db.Column(db.Date, nullable=True)
    created_at  = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.title} ({self.status})>'
