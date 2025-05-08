import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'gizli-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///crm.db'        # projenin kökünde crm.db dosyası oluşturur
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Uygulamada hangi modüller aktif olsun?
    ENABLED_MODULES = {
        'dashboard': 'Dashboard',
        'customers': 'Müşteriler',
        'stock': 'Stok',
        'messages': 'Mesajlar',
        'tasks': 'Görevler',
        'opportunities': 'Fırsatlar',
        'settings': 'Ayarlar',
        'auth': 'Kimlik'
    }
