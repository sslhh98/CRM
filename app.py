from flask import Flask, render_template, redirect, url_for, request
from flask_migrate import Migrate
from flask_login import LoginManager, login_required
from config import Config
from extensions import db

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(Config)

    # -- extensions --
    db.init_app(app)
    Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Lütfen giriş yapın.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        from modules.customers.models import Customer
        return Customer.query.get(int(user_id))

    # -- Blueprints --
    from modules.auth.routes          import auth_bp
    from modules.dashboard.routes     import dashboard_bp
    from modules.customers.routes     import customers_bp
    from modules.stock.routes         import stock_bp
    from modules.messages.routes      import messages_bp
    from modules.tasks.routes         import tasks_bp
    from modules.opportunities.routes import opportunities_bp
    from modules.settings.routes      import settings_bp

    app.register_blueprint(auth_bp,          url_prefix='/auth')
    app.register_blueprint(dashboard_bp,     url_prefix='/dashboard')
    app.register_blueprint(customers_bp,     url_prefix='/customers')
    app.register_blueprint(stock_bp,         url_prefix='/stock')
    app.register_blueprint(messages_bp,      url_prefix='/messages')
    app.register_blueprint(tasks_bp,         url_prefix='/tasks')
    app.register_blueprint(opportunities_bp, url_prefix='/opportunities')
    app.register_blueprint(settings_bp,      url_prefix='/settings')

    # -- Anasayfa yonlendirme --
    @app.route('/')
    @login_required
    def home():
        return redirect(url_for('dashboard.index'))

    # -- Global Arama --
    @app.route('/search')
    @login_required
    def global_search():
        from modules.customers.models      import Customer
        from modules.stock.models          import Stock
        from modules.messages.models       import Message
        from modules.tasks.models          import Task
        from modules.opportunities.models  import Opportunity

        q = request.args.get('q','').strip()
        if q:
            customers_res = Customer.query.filter(Customer.name.contains(q)).all()
            stocks_res    = Stock.query.filter(Stock.name.contains(q)).all()
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

    # -- Context processors --
    @app.context_processor
    def inject_modules_and_customers():
        from modules.customers.models import Customer
        try:
            customers = Customer.query.order_by(Customer.name).all()
        except:
            customers = []
        return {
            'all_customers': [{'id': c.id, 'name': c.name} for c in customers]
        }

    @app.context_processor
    def inject_activities():
        from modules.dashboard.models import Activity
        latest = Activity.query.order_by(Activity.timestamp.desc()).limit(10).all()
        return {'activities': latest}

    # -- Jinja Filter --
    from markupsafe import Markup
    import re
    @app.template_filter('linkify_tags')
    def linkify_tags(body):
        def repl(m):
            tag = m.group(1)
            href = url_for('messages.tag_filter', tag=tag)
            return f'<a href="{href}">#{tag}</a>'
        return Markup(re.sub(r'\B#(\w+)\b', repl, body))

    return app

if __name__ == '__main__':
    create_app().run(debug=True)
    # app = create_app()