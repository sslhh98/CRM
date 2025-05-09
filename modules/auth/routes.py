from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from extensions import db
from modules.customers.models import Customer

auth_bp = Blueprint('auth', __name__, template_folder='templates/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email','').strip()
        password = request.form.get('password','').strip()
        user = Customer.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Başarıyla giriş yapıldı.', 'success')
            return redirect(url_for('dashboard.index'))
        flash('Email veya şifre hatalı.', 'danger')
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Çıkış yapıldı.', 'info')
    return redirect(url_for('auth.login'))
