import pkgutil
import importlib
from flask import Flask, redirect, url_for
from flask_migrate import Migrate
from flask_login import LoginManager
from extensions import db
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # --- Extensions ---
    db.init_app(app)
    Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view            = 'auth.login'
    login_manager.login_message         = 'Lütfen giriş yapın.'
    login_manager.login_message_category= 'info'

    # kullanıcı loader
    from modules.customers.models import Customer as UserModel
    @login_manager.user_loader
    def load_user(user_id):
        return UserModel.query.get(int(user_id))

    # --- Blueprint'leri otomatik register ---
    import modules  # modules klasörü
    for finder, name, ispkg in pkgutil.iter_modules(modules.__path__):
        if not ispkg:
            continue
        mod_routes = importlib.import_module(f'modules.{name}.routes')
        bp = getattr(mod_routes, f'{name}_bp', None)
        if bp:
            app.register_blueprint(bp, url_prefix=f'/{name}')

    # Ana sayfa => Dashboard
    @app.route('/')
    def home():
        return redirect(url_for('dashboard.index'))

    return app

if __name__ == '__main__':
    create_app().run(debug=True)
