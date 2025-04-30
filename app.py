from flask import Flask, render_template, url_for, current_app, request
from flask_migrate import Migrate
from extensions import db
import importlib
from config import Config
from modules.dashboard.routes import dashboard_bp
from modules.settings.routes import settings_bp

# Modeller (global arama için)
from modules.customers.models    import Customer
from modules.stock.models        import Stock
from modules.messages.models     import Message
from modules.tasks.models        import Task
from modules.opportunities.models import Opportunity

app = Flask(__name__)
app.config.from_object(Config)

# DB & Migrate
db.init_app(app)
migrate = Migrate(app, db)

# Dinamik Blueprint kaydı
for mod_name, enabled in app.config['ENABLED_MODULES'].items():
    if enabled:
        module = importlib.import_module(f"modules.{mod_name}.routes")
        bp = getattr(module, f"{mod_name}_bp")
        app.register_blueprint(bp, url_prefix=f"/{mod_name}")

# Ayarlar sayfasını her zaman ekle
app.register_blueprint(settings_bp, url_prefix='/settings')

# Tüm şablonlara 'modules' değişkenini enjekte et
@app.context_processor
def inject_modules():
    return {'modules': current_app.config['ENABLED_MODULES']}

# Anasayfa
@app.route('/')
def home():
    return render_template('index.html')

# --- linkify_tags filtre ---
from markupsafe import Markup
import re

@app.template_filter('linkify_tags')
def linkify_tags(body):
    def repl(match):
        tag = match.group(1)
        href = url_for('messages.tag_filter', tag=tag)
        return f'<a href="{ href }">#{ tag }</a>'
    return Markup(re.sub(r'\B#(\w+)\b', repl, body))

# --- Global Arama ---
@app.route('/search')
def global_search():
    q = request.args.get('q', '').strip()
    customers     = Customer.query.filter(Customer.name.contains(q)).all()      if q else []
    stocks        = Stock.query.filter(Stock.size.contains(q)).all()           if q else []
    messages      = Message.query.filter(Message.body.contains(q)).all()       if q else []
    tasks         = Task.query.filter(Task.title.contains(q)).all()            if q else []
    opportunities = Opportunity.query.filter(Opportunity.name.contains(q)).all() if q else []
    return render_template('search_results.html',
                           query=q,
                           customers=customers,
                           stocks=stocks,
                           messages=messages,
                           tasks=tasks,
                           opportunities=opportunities)

if __name__ == '__main__':
    # İsterseniz her çalıştırmada DB'yi resetlemek için:
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug=True)
    # app.run(debug=True, host='