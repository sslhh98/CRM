from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from modules.stock.models import Stock
from extensions import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from modules.dashboard.models import Activity

stock_bp = Blueprint('stock', __name__, url_prefix='/stock')

@stock_bp.route('/', endpoint='index')
@stock_bp.route('/list', endpoint='stock_list')
def stock_list():
    q = request.args.get('q','').strip()
    if q:
        stocks = Stock.query.filter(Stock.size.contains(q)).order_by(Stock.id.desc()).all()
    else:
        stocks = Stock.query.order_by(Stock.id.desc()).all()
    return render_template('stock_list.html', stocks=stocks, search=q)

@stock_bp.route('/add', methods=['GET','POST'], endpoint='add_stock')
def add_stock():
    if request.method=='POST':
        size = request.form.get('size','').strip()
        qty  = request.form.get('quantity','').strip()
        if not (size and qty.isdigit()):
            flash("Boyut ve miktarı doğru girin.", "error")
            return redirect(url_for('stock.add_stock'))
        new = Stock(size=size, quantity=int(qty), last_updated=datetime.utcnow())
        db.session.add(new)
        try:
            db.session.commit()
            # Activity kaydı
            act = Activity(
                user_id=current_user.id,
                customer_id=None,
                action=f"Yeni stok kaydı: “{size}” × {qty} eklendi."
            )
            db.session.add(act)
            db.session.commit()

            flash("Yeni stok eklendi.", "success")
        except IntegrityError:
            db.session.rollback()
            flash("Stok eklerken hata oluştu.", "error")
        return redirect(url_for('stock.stock_list'))
    return render_template('add_stock.html')

@stock_bp.route('/update/<int:id>', methods=['GET','POST'], endpoint='update_stock')
def update_stock(id):
    s = Stock.query.get_or_404(id)
    if request.method=='POST':
        qty = request.form.get('quantity','').strip()
        if qty.isdigit():
            old = s.quantity
            s.quantity = int(qty)
            s.last_updated = datetime.utcnow()
            db.session.commit()
            # Activity kaydı
            act = Activity(
                user_id=current_user.id,
                customer_id=None,
                action=f"Stok “{s.size}” miktarı {old}→{qty} güncellendi."
            )
            db.session.add(act)
            db.session.commit()

            flash("Stok güncellendi.", "success")
        else:
            flash("Geçerli bir miktar girin.", "error")
        return redirect(url_for('stock.stock_list'))
    return render_template('update_stock.html', stock=s)

@stock_bp.route('/delete/<int:id>', endpoint='delete_stock')
def delete_stock(id):
    s = Stock.query.get_or_404(id)
    size = s.size
    db.session.delete(s)
    db.session.commit()
    # Activity kaydı
    act = Activity(
        user_id=current_user.id,
        customer_id=None,
        action=f"Stok “{size}” silindi."
    )
    db.session.add(act)
    db.session.commit()

    flash("Stok kaydı silindi.", "success")
    return redirect(url_for('stock.stock_list'))
