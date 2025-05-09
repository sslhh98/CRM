from flask import Blueprint, render_template
from flask_login import login_required
from modules.customers.models      import Customer
from modules.stock.models          import Stock
from modules.messages.models       import Message
from modules.tasks.models          import Task
from modules.opportunities.models  import Opportunity

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    total_customers   = Customer.query.count()
    total_stock_items = Stock.query.count()
    total_messages    = Message.query.count()
    total_tasks       = Task.query.count()
    total_opps        = Opportunity.query.count()
    return render_template(
        'dashboard/index.html',
        total_customers=total_customers,
        total_stock_items=total_stock_items,
        total_messages=total_messages,
        total_tasks=total_tasks,
        total_opps=total_opps
    )
