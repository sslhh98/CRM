
# modules/customers/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, make_response
from flask_login import current_user
from sqlalchemy.exc import IntegrityError
from extensions import db
from modules.customers.models import Customer
from modules.dashboard.models import Activity
import io, csv

customers_bp = Blueprint('customers', __name__, url_prefix='/customers')

# ─── ANA EKRAN: Form + Liste ───
@customers_bp.route('/', methods=['GET','POST'], endpoint='index')
def index():
    search = request.args.get('q','').strip()

    if request.method == 'POST':
        name    = request.form.get('name','').strip()
        phone   = request.form.get('phone','').strip()
        email   = request.form.get('email','').strip()
        status  = request.form.get('status','').strip()
        tag     = request.form.get('tag','').lstrip('#').strip()

        if not all([name, phone, email, status, tag]):
            flash('Lütfen tüm alanları doldurun; özellikle Etiket’i.', 'error')
            return redirect(url_for('customers.index'))

        yeni = Customer(name=name, phone=phone, email=email, status=status, tag=tag)
        db.session.add(yeni)
        try:
            db.session.commit()
            if current_user.is_authenticated:
                act = Activity(
                    user_id=current_user.id,
                    customer_id=yeni.id,
                    action=f"Yeni müşteri “{yeni.name}” eklendi."
                )
                db.session.add(act)
                db.session.commit()
            flash('Yeni müşteri başarıyla eklendi.', 'success')
        except IntegrityError:
            db.session.rollback()
            flash(f"#{tag} etiketi zaten kullanılıyor.", 'error')
        return redirect(url_for('customers.index'))

    if search:
        customers = (Customer.query
                       .filter(Customer.name.contains(search))
                       .order_by(Customer.name)
                       .all())
    else:
        customers = Customer.query.order_by(Customer.name).all()

    return render_template('customers_index.html', customers=customers, search=search)

# ─── CSV EXPORT ───
@customers_bp.route('/export', methods=['GET'], endpoint='export_customers')
def export_customers():
    customers = Customer.query.order_by(Customer.name).all()
    si = io.StringIO()
    writer = csv.writer(si)
    writer.writerow(['id','name','phone','email','status','tag'])
    for c in customers:
        writer.writerow([c.id, c.name, c.phone, c.email, c.status, c.tag])
    output = make_response(si.getvalue())
    output.headers['Content-Disposition'] = 'attachment; filename=customers.csv'
    output.headers['Content-Type'] = 'text/csv'
    return output

# ─── CSV IMPORt ───
@customers_bp.route('/import', methods=['GET','POST'], endpoint='import_customers')
def import_customers():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file:
            flash('Lütfen bir CSV dosyası seçin.', 'error')
            return redirect(url_for('customers.import_customers'))

        stream = io.StringIO(file.stream.read().decode('utf-8'), newline=None)
        reader = csv.DictReader(stream)
        count = 0
        for row in reader:
            try:
                c = Customer(
                    name=row['name'].strip(),
                    phone=row['phone'].strip(),
                    email=row['email'].strip(),
                    status=row['status'].strip(),
                    tag=row['tag'].strip()
                )
                db.session.add(c)
                db.session.flush()  # get id if needed
                if current_user.is_authenticated:
                    act = Activity(
                        user_id=current_user.id,
                        customer_id=c.id,
                        action=f"Müşteri “{c.name}” içe aktarıldı."
                    )
                    db.session.add(act)
                count += 1
            except Exception:
                db.session.rollback()
                continue
        db.session.commit()
        flash(f"{count} müşteri başarıyla içe aktarıldı.", 'success')
        return redirect(url_for('customers.index'))

    return render_template('import_customers.html')

# ─── INLINE EKLEME ───
@customers_bp.route('/add_inline', methods=['POST'], endpoint='add_inline')
def add_inline():
    data = request.get_json() or {}
    name = (data.get('name') or '').strip()
    if not name:
        return jsonify({'error':'İsim boş'}), 400

    cust = Customer(name=name, phone='', email='', status='', tag='')
    db.session.add(cust)
    try:
        db.session.commit()
        if current_user.is_authenticated:
            act = Activity(
                user_id=current_user.id,
                customer_id=cust.id,
                action=f"Yeni müşteri “{cust.name}” eklendi."
            )
            db.session.add(act)
            db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error':'Etiket çakışması'}), 400

    return jsonify({'id':cust.id,'name':cust.name})

# ─── DÜZENLEME ───
@customers_bp.route('/edit/<int:id>', methods=['GET','POST'], endpoint='edit_customer')
def edit_customer(id):
    c = Customer.query.get_or_404(id)
    if request.method=='POST':
        name    = request.form.get('name','').strip()
        phone   = request.form.get('phone','').strip()
        email   = request.form.get('email','').strip()
        status  = request.form.get('status','').strip()
        tag     = request.form.get('tag','').lstrip('#').strip()

        if not all([name, phone, email, status, tag]):
            flash('Lütfen tüm alanları doldurun; özellikle Etiket’i.', 'error')
            return redirect(url_for('customers.edit_customer', id=id))

        if tag != c.tag and Customer.query.filter(Customer.tag==tag, Customer.id!=id).first():
            flash(f"#{tag} etiketi zaten kullanılıyor.", 'error')
            return redirect(url_for('customers.edit_customer', id=id))

        c.name, c.phone, c.email, c.status, c.tag = name, phone, email, status, tag
        try:
            db.session.commit()
            if current_user.is_authenticated:
                act = Activity(
                    user_id=current_user.id,
                    customer_id=c.id,
                    action=f"Müşteri “{c.name}” güncellendi."
                )
                db.session.add(act)
                db.session.commit()
            flash('Müşteri başarıyla güncellendi.', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Bir hata oluştu, tekrar deneyin.', 'error')
        return redirect(url_for('customers.index'))
    return render_template('edit_customer.html', customer=c)

# ─── SİLME ───
@customers_bp.route('/delete/<int:id>', endpoint='delete_customer')
def delete_customer(id):
    c = Customer.query.get_or_404(id)
    name = c.name
    db.session.delete(c)
    db.session.commit()
    if current_user.is_authenticated:
        act = Activity(
            user_id=current_user.id,
            customer_id=id,
            action=f"Müşteri “{name}” silindi."
        )
        db.session.add(act)
        db.session.commit()

    flash('Müşteri silindi.', 'success')
    return redirect(url_for('customers.index'))
