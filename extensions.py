# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def init_app(app):
    db.init_app(app)
    login_manager.init_app(app)
    # Giriş sayfası rotasını belirtmek isterseniz:
    # login_manager.login_view = 'auth.login'
