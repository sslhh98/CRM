from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from modules.stock.models import Stock
from extensions import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from modules.dashboard.models import Activity

stock_bp = Blueprint('stock', __name__, url_prefix='/stock')

# modules/stock/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from extensions import db
from .models import Stock

stock_bp = Blueprint('stock', __name__)

@stock_bp.route('/')
def index():
    items = Stock.query.all()
    return render_template('stock_index.html', stocks=items)

@stock_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        size = request.form['size'].strip()
        qty  = int(request.form['quantity'])
        s = Stock(size=size, quantity=qty)
        db.session.add(s)
        db.session.commit()
        flash('Stok kaydı eklendi.', 'success')
        return redirect(url_for('stock.index'))
    return render_template('add_stock.html')

@stock_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    s = Stock.query.get_or_404(id)
    if request.method == 'POST':
        s.size = request.form['size'].strip()
        s.quantity = int(request.form['quantity'])
        db.session.commit()
        flash('Stok kaydı güncellendi.', 'success')
        return redirect(url_for('stock.index'))
    return render_template('edit_stock.html', stock=s)

@stock_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    s = Stock.query.get_or_404(id)
    db.session.delete(s)
    db.session.commit()
    flash('Stok kaydı silindi.', 'info')
    return redirect(url_for('stock.index'))
