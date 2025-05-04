from flask import Blueprint, render_template
from modules.customers.models import Customer
from modules.stock.models import Stock
from modules.messages.models import Message
from modules.tasks.models import Task
from modules.opportunities.models import Opportunity

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')

@dashboard_bp.route('/', endpoint='index')
def index():
    # Temel metrikler
    total_customers = Customer.query.count()
    total_stocks    = Stock.query.count()
    total_messages  = Message.query.count()

    # Görev durumlarına göre sayaçlar
    tasks_status_counts = {
        'Beklemede':    Task.query.filter_by(status='Beklemede').count(),
        'Devam Ediyor': Task.query.filter_by(status='Devam').count(),
        'Tamamlandı':   Task.query.filter_by(status='Tamamlandı').count()
    }

    # Fırsat aşamalarına göre sayaçlar
    STAGES = ['İlk Temas', 'Teklif Verildi', 'Görüşme', 'Kapanış', 'Kaybedildi']
    opp_stage_counts = {
        stage: Opportunity.query.filter_by(stage=stage).count()
        for stage in STAGES
    }

    return render_template(
        'dashboard_index.html',
        total_customers=total_customers,
        total_stocks=total_stocks,
        total_messages=total_messages,
        tasks_status_counts=tasks_status_counts,
        opp_stage_counts=opp_stage_counts
    )
