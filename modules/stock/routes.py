from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from extensions import db
from modules.stock.models import Stock

stock_bp = Blueprint('stock', __name__, template_folder='templates/stock')

@stock_bp.route('/')
@login_required
def index():
    items = Stock.query.all()
    return render_template('stock/index.html', stocks=items)

@stock_bp.route('/create', methods=['GET','POST'])
@login_required
def create():
    if request.method == 'POST':
        name     = request.form['name']
        quantity = int(request.form['quantity'])
        s = Stock(name=name, quantity=quantity)
        db.session.add(s)
        db.session.commit()
        flash('Stok kalemi eklendi.', 'success')
        return redirect(url_for('stock.index'))
    return render_template('stock/create.html')

@stock_bp.route('/<int:id>/edit', methods=['GET','POST'])
@login_required
def edit(id):
    s = Stock.query.get_or_404(id)
    if request.method == 'POST':
        s.name     = request.form['name']
        s.quantity = int(request.form['quantity'])
        db.session.commit()
        flash('Güncellendi.', 'success')
        return redirect(url_for('stock.index'))
    return render_template('stock/edit.html', stock=s)

@stock_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    s = Stock.query.get_or_404(id)
    db.session.delete(s)
    db.session.commit()
    flash('Silindi.', 'info')
    return redirect(url_for('stock.index'))
