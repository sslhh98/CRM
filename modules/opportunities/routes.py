from flask import Blueprint, render_template, request, redirect, url_for, flash
from modules.opportunities.models import Opportunity
from modules.customers.models import Customer
from extensions import db
from datetime import datetime

opportunities_bp = Blueprint('opportunities', __name__)

STAGES = ['İlk Temas','Teklif Verildi','Görüşme','Kapanış','Kaybedildi']

# Listeleme + Arama + Yeni fırsat ekleme
@opportunities_bp.route('/', methods=['GET','POST'], endpoint='index')
def index():
    if request.method == 'POST':
        name       = request.form.get('name','').strip()
        cust_id    = request.form.get('customer_id') or None
        stage      = request.form.get('stage')
        value      = request.form.get('value') or None
        close_date = request.form.get('close_date') or None

        if not name:
            flash("Fırsat başlığını girin.", "error")
            return redirect(url_for('opportunities.index'))

        opp = Opportunity(
            name=name,
            customer_id=int(cust_id) if cust_id else None,
            stage=stage,
            value=float(value) if value else None,
            close_date=(datetime.strptime(close_date, '%Y-%m-%d')
                        if close_date else None)
        )
        db.session.add(opp)
        db.session.commit()
        flash("Yeni fırsat eklendi.", "success")
        return redirect(url_for('opportunities.index'))

    # GET: arama varsa filtrele
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

# Fırsat aşaması güncelleme
@opportunities_bp.route('/update/<int:id>', methods=['POST'], endpoint='update_opportunity')
def update_opportunity(id):
    opp = Opportunity.query.get_or_404(id)
    new_stage = request.form.get('stage')
    if new_stage in STAGES:
        opp.stage = new_stage
        db.session.commit()
        flash("Fırsat aşaması güncellendi.", "success")
    return redirect(url_for('opportunities.index'))

# Fırsat silme
@opportunities_bp.route('/delete/<int:id>', endpoint='delete_opportunity')
def delete_opportunity(id):
    opp = Opportunity.query.get_or_404(id)
    db.session.delete(opp)
    db.session.commit()
    flash("Fırsat silindi.", "success")
    return redirect(url_for('opportunities.index'))
