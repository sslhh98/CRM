# modules/dashboard/models.py
from extensions import db
from datetime import datetime

class Activity(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    user_id   = db.Column(db.Integer, nullable=False)
    module    = db.Column(db.String(50), nullable=False)
    action    = db.Column(db.String(200), nullable=False)
    item_id   = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
