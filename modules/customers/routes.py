from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from extensions import db
from modules.customers.models import Customer

customers_bp = Blueprint('customers', __name__, template_folder='templates/customers')

@customers_bp.route('/')
@login_required
def index():
    all_customers = Customer.query.order_by(Customer.name).all()
    return render_template('customers/index.html', customers=all_customers)

@customers_bp.route('/create', methods=['GET','POST'])
@login_required
def create():
    if request.method == 'POST':
        name  = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        c = Customer(name=name, email=email, phone=phone)
        db.session.add(c)
        db.session.commit()
        flash('Müşteri eklendi.', 'success')
        return redirect(url_for('customers.index'))
    return render_template('customers/create.html')

@customers_bp.route('/<int:id>/edit', methods=['GET','POST'])
@login_required
def edit(id):
    c = Customer.query.get_or_404(id)
    if request.method == 'POST':
        c.name  = request.form['name']
        c.email = request.form['email']
        c.phone = request.form['phone']
        db.session.commit()
        flash('Güncellendi.', 'success')
        return redirect(url_for('customers.index'))
    return render_template('customers/edit.html', customer=c)

@customers_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    c = Customer.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()
    flash('Silindi.', 'info')
    return redirect(url_for('customers.index'))
