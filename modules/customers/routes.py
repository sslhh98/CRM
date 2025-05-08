# modules/customers/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from extensions import db
from .models import Customer

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/')
def index():
    all_customers = Customer.query.order_by(Customer.name).all()
    return render_template('customers_index.html', customers=all_customers)

@customers_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        c = Customer(name=name, email=email)
        db.session.add(c)
        db.session.commit()
        flash('Müşteri eklendi.', 'success')
        return redirect(url_for('customers.index'))
    return render_template('add_customer.html')

@customers_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    c = Customer.query.get_or_404(id)
    if request.method == 'POST':
        c.name = request.form['name'].strip()
        c.email = request.form['email'].strip()
        db.session.commit()
        flash('Müşteri güncellendi.', 'success')
        return redirect(url_for('customers.index'))
    return render_template('edit_customer.html', customer=c)

@customers_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    c = Customer.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()
    flash('Müşteri silindi.', 'info')
    return redirect(url_for('customers.index'))
