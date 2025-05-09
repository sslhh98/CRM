from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from extensions import db
from modules.settings.models import Setting

settings_bp = Blueprint('settings', __name__, template_folder='templates/settings')

@settings_bp.route('/')
@login_required
def index():
    settings = Setting.query.all()
    return render_template('settings/index.html', settings=settings)

@settings_bp.route('/<int:id>/edit', methods=['GET','POST'])
@login_required
def edit(id):
    s = Setting.query.get_or_404(id)
    if request.method == 'POST':
        s.value = request.form['value']
        db.session.commit()
        flash('Ayar kaydedildi.', 'success')
        return redirect(url_for('settings.index'))
    return render_template('settings/edit.html', setting=s)
