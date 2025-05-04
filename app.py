from flask import Flask, render_template, url_for, current_app, request, redirect
from flask_migrate import Migrate
from flask_login import LoginManager
from extensions import db
import importlib
from config import Config
# app.py
# …
# Blueprint’leri, extensions vs. import ettikten hemen sonra:
import modules.dashboard.models  # Activity model’i burada kaydedilmiş olur
from modules.dashboard.models import Activity
from modules.customers.models import Customer
from modules.stock.models import Stock
from modules.messages.models import Message
from modules.tasks.models import Task
from modules.opportunities.models import Opportunity

# Flask uygulaması oluşturma
app = Flask(__name__)
app.config.from_object(Config)

# Uzantıları init et
db.init_app(app)
migrate = Migrate(app, db)

# Flask-Login ayarları
login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view = 'auth.login'

# User loader callback
from modules.customers.models import Customer as UserModel
@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))

# Blueprint’ler
to_register = ['dashboard', 'customers', 'stock', 'messages', 'tasks', 'opportunities']
for mod_name in to_register:
    try:
        module = importlib.import_module(f"modules.{mod_name}.routes")
        bp = getattr(module, f"{mod_name}_bp")
        app.register_blueprint(bp, url_prefix=f"/{mod_name}")
    except (ImportError, AttributeError):
        pass

# Ayarlar sayfasını her zaman ekle
from modules.settings.routes import settings_bp
app.register_blueprint(settings_bp, url_prefix='/settings')

# Modeller (global arama için)
from modules.customers.models      import Customer
from modules.stock.models          import Stock
from modules.messages.models       import Message
from modules.tasks.models          import Task
from modules.opportunities.models  import Opportunity

# Context Processor’lar
@app.context_processor
def inject_customers_and_modules():
    modules = current_app.config.get('ENABLED_MODULES', {})
    try:
        customers = Customer.query.order_by(Customer.name).all()
    except Exception:
        customers = []
    return {
        'modules': modules,
        'all_customers': [{'id': c.id, 'name': c.name} for c in customers]
    }

@app.context_processor
def inject_activities():
    from sqlalchemy import inspect
    from modules.dashboard.models import Activity
    latest_activities = []
    try:
        inspector = inspect(db.engine)
        if 'activities' in inspector.get_table_names():
            latest_activities = (
                Activity.query
                        .order_by(Activity.timestamp.desc())
                        .limit(10)
                        .all()
            )
    except Exception:
        pass
    return {'latest_activities': latest_activities}

# Anasayfa: Dashboard’a yönlendir
@app.route('/')
def home():
    return redirect(url_for('dashboard.index'))

# Genel Arama
@app.route('/search')
def global_search():
    q = request.args.get('q', '').strip()
    if q:
        customers_res = Customer.query.filter(Customer.name.contains(q)).all()
        stocks_res    = Stock.query.filter(Stock.size.contains(q)).all()
        messages_res  = Message.query.filter(Message.body.contains(q)).all()
        tasks_res     = Task.query.filter(Task.title.contains(q)).all()
        opps_res      = Opportunity.query.filter(Opportunity.name.contains(q)).all()
    else:
        customers_res = stocks_res = messages_res = tasks_res = opps_res = []
    return render_template(
        'search_results.html',
        query=q,
        customers=customers_res,
        stocks=stocks_res,
        messages=messages_res,
        tasks=tasks_res,
        opportunities=opps_res
    )

# Jinja Filter: #tag linkify
from markupsafe import Markup
import re
@app.template_filter('linkify_tags')
def linkify_tags(body):
    def repl(match):
        tag = match.group(1)
        href = url_for('messages.tag_filter', tag=tag)
        return f'<a href="{href}">#{tag}</a>'
    return Markup(re.sub(r'\B#(\w+)\b', repl, body))

if __name__ == '__main__':
    app.run(debug=True)