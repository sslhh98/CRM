import os, json
from flask import Blueprint, render_template, request, redirect, url_for, current_app

settings_bp = Blueprint('settings', __name__, template_folder='templates')

@settings_bp.route('/', methods=['GET', 'POST'])
def index():
    cfg = current_app.config
    path = cfg['MODULES_PATH']

    if request.method == 'POST':
        # Form’da işaretli olan modülleri oku
        new_mods = {}
        for mod in cfg['ENABLED_MODULES'].keys():
            # checkbox on ise request.form’da yer alır
            new_mods[mod] = (mod in request.form)
        # modules.json’u güncelle
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(new_mods, f, indent=2, ensure_ascii=False)
        # runtime konfigürasyonu yenile
        cfg['ENABLED_MODULES'] = new_mods
        return redirect(url_for('settings.index'))

    return render_template('settings.html', modules=cfg['ENABLED_MODULES'])
