from flask import Blueprint, render_template
from modules.customers.models      import Customer
from modules.stock.models          import Stock
from modules.messages.models       import Message
from modules.tasks.models          import Task
from modules.opportunities.models  import Opportunity

dashboard_bp = Blueprint(
    'dashboard',         # endpoint prefix için kullanılacak isim
    __name__,
    template_folder='templates/dashboard'
)

@dashboard_bp.route('/', methods=['GET'])
def index():
    total_customers     = Customer.query.count()
    total_stocks        = Stock.query.count()
    total_messages      = Message.query.count()
    total_tasks         = Task.query.count()
    total_opportunities = Opportunity.query.count()
    return render_template(
        'dashboard_index.html',
        total_customers=total_customers,
        total_stocks=total_stocks,
        total_messages=total_messages,
        total_tasks=total_tasks,
        total_opportunities=total_opportunities
    )
