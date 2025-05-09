from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from extensions import db
from modules.opportunities.models import Opportunity
from modules.customers.models import Customer

opportunities_bp = Blueprint('opportunities', __name__, template_folder='templates/opportunities')

@opportunities_bp.route('/')
@login_required
def index():
    opps = Opportunity.query.order_by(Opportunity.created_at.desc()).all()
    return render_template('opportunities/index.html', opportunities=opps)

@opportunities_bp.route('/create', methods=['GET','POST'])
@login_required
def create():
    customers = Customer.query.all()
    if request.method == 'POST':
        name        = request.form['name']
        value       = float(request.form['value'])
        customer_id = int(request.form['customer_id'])
        o = Opportunity(name=name, value=value, customer_id=customer_id)
        db.session.add(o)
        db.session.commit()
        flash('Fırsat eklendi.', 'success')
        return redirect(url_for('opportunities.index'))
    return render_template('opportunities/create.html', customers=customers)
