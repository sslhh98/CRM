from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from modules.opportunities.models import Opportunity
from modules.customers.models import Customer
from extensions import db
from datetime import datetime
from modules.dashboard.models import Activity

# Define the stages for opportunities
STAGES = ['New', 'In Progress', 'Won', 'Lost']

# modules/opportunities/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from extensions import db
from .models import Opportunity

opportunities_bp = Blueprint('opportunities', __name__)

@opportunities_bp.route('/')
def index():
    opps = Opportunity.query.order_by(Opportunity.created_at.desc()).all()
    return render_template('opportunities_index.html', opportunities=opps)

@opportunities_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name   = request.form['name'].strip()
        stage  = request.form['stage'].strip()
        o = Opportunity(name=name, stage=stage)
        db.session.add(o)
        db.session.commit()
        flash('Fırsat eklendi.', 'success')
        return redirect(url_for('opportunities.index'))
    return render_template('add_opportunity.html')


    q = request.args.get('q','').strip()
    if q:
        opportunities = (Opportunity.query
                            .filter(Opportunity.name.contains(q))
                            .order_by(Opportunity.created_at.desc())
                            .all())
    else:
        opportunities = Opportunity.query.order_by(Opportunity.created_at.desc()).all()

    customers = Customer.query.all()
    return render_template('opportunities_index.html',
                           opportunities=opportunities,
                           customers=customers,
                           stages=STAGES,
                           search=q)

@opportunities_bp.route('/update/<int:id>', methods=['POST'], endpoint='update_opportunity')
def update_opportunity(id):
    opp = Opportunity.query.get_or_404(id)
    new_stage = request.form.get('stage')
    if new_stage in STAGES:
        opp.stage = new_stage
        db.session.commit()
        # Activity kaydı
        act = Activity(
            user_id=current_user.id,
            customer_id=opp.customer_id,
            action=f"Fırsat “{opp.name}” aşaması “{new_stage}” yapıldı."
        )
        db.session.add(act)
        db.session.commit()

        flash("Fırsat aşaması güncellendi.", "success")
    return redirect(url_for('opportunities.index'))

@opportunities_bp.route('/delete/<int:id>', endpoint='delete_opportunity')
def delete_opportunity(id):
    opp = Opportunity.query.get_or_404(id)
    name = opp.name
    db.session.delete(opp)
    db.session.commit()
    # Activity kaydı
    act = Activity(
        user_id=current_user.id,
        customer_id=opp.customer_id,
        action=f"Fırsat “{name}” silindi."
    )
    db.session.add(act)
    db.session.commit()

    flash("Fırsat silindi.", "success")
    return redirect(url_for('opportunities.index'))
