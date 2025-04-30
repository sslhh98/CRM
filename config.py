import os, json

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///crm.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # modules.json yolu
    MODULES_PATH = os.path.join(os.path.dirname(__file__), 'modules.json')

    # modules.json’dan aktif modülleri oku
    with open(MODULES_PATH, 'r', encoding='utf-8') as f:
        ENABLED_MODULES = json.load(f)
