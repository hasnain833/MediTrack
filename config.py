import os


DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'medical_user',
    'password': 'your_password',
    'database': 'medical_store',
    'raise_on_warnings': True
}


APP_NAME = "D. Chemist"  
APP_VERSION = "1.0.0"
COMPANY_NAME = "D. Chemist"


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
ICONS_DIR = os.path.join(ASSETS_DIR, 'icons')
INVOICES_DIR = os.path.join(BASE_DIR, 'invoices')
BACKUPS_DIR = os.path.join(BASE_DIR, 'backups')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

GST_RATE = 12
LOW_STOCK_THRESHOLD = 10
EXPIRY_WARNING_DAYS = 30
SESSION_TIMEOUT = 30