# modules/customers/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from modules.customers.models import Customer
from extensions import db
from sqlalchemy.exc import IntegrityError
import io
import csv

customers_bp = Blueprint('customers', __name__)

# ─── ANA EKRAN: Form + Liste ───
@customers_bp.route('/', methods=['GET', 'POST'], endpoint='index')
def index():
    search = request.args.get('q', '')

    if request.method == 'POST':
        # 1️⃣ Form’dan gelen verileri al ve temizle
        name    = request.form.get('name', '').strip()
        phone   = request.form.get('phone', '').strip()
        email   = request.form.get('email', '').strip()
        status  = request.form.get('status', '').strip()
        raw_tag = request.form.get('tag', '').strip()

        # 2️⃣ “#” işaretini kaldır
        tag = raw_tag.lstrip('#')

        # 3️⃣ Zorunlu alanlar dolu mu?
        if not (name and phone and email and status and tag):
            flash("Lütfen tüm alanları doldurun; özellikle Etiket’i.", "error")
            return redirect(url_for('customers.index'))

        # 4️⃣ Yeni müşteri oluşturup kaydet, hata yakala
        yeni = Customer(name=name, phone=phone, email=email, status=status, tag=tag)
        db.session.add(yeni)
        try:
            db.session.commit()
            flash("Yeni müşteri başarıyla eklendi.", "success")
        except IntegrityError:
            db.session.rollback()
            flash(f"#{tag} etiketi zaten kullanılıyor. Lütfen başka bir etiket seçin.", "error")

        return redirect(url_for('customers.index'))

    # GET: Listeleme (arama varsa filtrele)
    if search:
        customers = Customer.query.filter(Customer.name.contains(search)).all()
    else:
        customers = Customer.query.all()

    return render_template(
        'customers_index.html',
        customers=customers,
        search=search
    )


# ─── Salt Liste Sayfası ───
@customers_bp.route('/list', endpoint='customer_list')
def customer_list():
    customers = Customer.query.all()
    return render_template('customers_list.html', customers=customers)


# ─── Düzenleme ───
@customers_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    c = Customer.query.get_or_404(id)

    if request.method == 'POST':
        # 1️⃣ Form’dan gelen değerler
        name    = request.form.get('name', '').strip()
        phone   = request.form.get('phone', '').strip()
        email   = request.form.get('email', '').strip()
        status  = request.form.get('status', '').strip()
        raw_tag = request.form.get('tag', '').strip()
        tag     = raw_tag.lstrip('#')

        # 2️⃣ Zorunlu alan kontrolü
        if not (name and phone and email and status and tag):
            flash("Lütfen tüm alanları doldurun; özellikle Etiket’i.", "error")
            return redirect(url_for('customers.edit_customer', id=id))

        # 3️⃣ Eğer etiket değiştiyse benzersizlik kontrolü
        if tag != c.tag:
            exists = Customer.query.filter(Customer.tag == tag, Customer.id != id).first()
            if exists:
                flash(f"#{tag} etiketi zaten başka bir müşteride kullanılıyor.", "error")
                return redirect(url_for('customers.edit_customer', id=id))

        # 4️⃣ Atamaları yap ve commit et
        c.name   = name
        c.phone  = phone
        c.email  = email
        c.status = status
        c.tag    = tag

        try:
            db.session.commit()
            flash("Müşteri başarıyla güncellendi.", "success")
        except IntegrityError:
            db.session.rollback()
            flash("Bir hata oluştu, lütfen tekrar deneyin.", "error")

        return redirect(url_for('customers.index'))

    # GET: Formu mevcut verilerle göster
    return render_template('edit_customer.html', customer=c)


# ─── Silme ───
@customers_bp.route('/delete/<int:id>')
def delete_customer(id):
    c = Customer.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()
    flash("Müşteri silindi.", "success")
    return redirect(url_for('customers.index'))

@customers_bp.route('/export', methods=['GET'])
def export_customers():
    customers = Customer.query.all()
    si = io.StringIO()
    writer = csv.writer(si)
    writer.writerow(['id','name','phone','email','status','tag'])
    for c in customers:
        writer.writerow([c.id, c.name, c.phone, c.email, c.status, c.tag])
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=customers.csv"
    output.headers["Content-type"] = "text/csv"
    return output

# ─── IMPORT (CSV) ───
@customers_bp.route('/import', methods=['GET','POST'])
def import_customers():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file:
            flash("Lütfen bir CSV dosyası seçin.", "error")
            return redirect(url_for('customers.import_customers'))

        stream = io.StringIO(file.stream.read().decode("utf-8"), newline=None)
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
                count += 1
            except Exception:
                db.session.rollback()
                continue
        db.session.commit()
        flash(f"{count} müşteri başarıyla içe aktarıldı.", "success")
        return redirect(url_for('customers.index'))

    return render_template('import_customers.html')