# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime

db = SQLAlchemy()
login_manager = LoginManager()

def init_app(app):
    db.init_app(app)
    login_manager.init_app(app)
    # login_manager.login_view = 'auth.login'  # Giriş sayfası route’u

def log_activity(user_id, module_name, action, item_id=None):
    """
    Kullanıcı aktivitelerini dashboard zaman tüneline kaydeder.
    :param user_id: int
    :param module_name: str, 'messages', 'tasks', vb.
    :param action: str, örn. 'create', 'update', 'delete' veya özgün açıklama
    :param item_id: int veya None
    """
    # Burada import ederek döngüyü kırıyoruz
    from modules.dashboard.models import Activity

    activity = Activity(
        user_id=user_id,
        module=module_name,
        action=action,
        item_id=item_id,
        timestamp=datetime.utcnow()
    )
    db.session.add(activity)
    db.session.commit()
