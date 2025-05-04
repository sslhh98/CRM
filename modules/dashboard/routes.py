from flask import Blueprint, render_template
from modules.customers.models      import Customer
from modules.stock.models          import Stock
from modules.messages.models       import Message
from modules.tasks.models          import Task
from modules.opportunities.models  import Opportunity
from modules.dashboard.models      import Activity
from extensions                     import db
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/', methods=['GET'], endpoint='index')
def index():
    # Metrikler
    total_customers = Customer.query.count()
    total_stocks    = Stock.query.count()
    total_messages  = Message.query.count()

    # Son 10 activity kaydı
    activities = (
        Activity.query
                .order_by(Activity.timestamp.desc())
                .limit(10)
                .all()
    )

    # Tasks durumları (group by status)
    tasks_status_counts = dict(
        db.session
          .query(Task.status, func.count(Task.id))
          .group_by(Task.status)
          .all()
    )

    # Opportunities aşamaları (group by stage)
    opp_stage_counts = dict(
        db.session
          .query(Opportunity.stage, func.count(Opportunity.id))
          .group_by(Opportunity.stage)
          .all()
    )

    return render_template(
        'dashboard_index.html',
        total_customers=total_customers,
        total_stocks=total_stocks,
        total_messages=total_messages,
        activities=activities,
        tasks_status_counts=tasks_status_counts,
        opp_stage_counts=opp_stage_counts,
    )
