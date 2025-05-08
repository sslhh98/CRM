import os, json
# modules/settings/routes.py
from flask import Blueprint, render_template, request, flash, redirect, url_for

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # burada form ile gelen ayarları kaydet
        flash('Ayarlar kaydedildi.', 'success')
        return redirect(url_for('settings.index'))
    # mevcut ayarları config veya DB’den çekip ver
    return render_template('settings.html')
