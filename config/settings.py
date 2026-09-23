import os


class Config:
    """Конфигурация приложения"""
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'database.db')
    API_BASE_URL = os.getenv('API_BASE_URL', 'http://127.0.0.1:10000/api')
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    FLASK_PORT = int(os.getenv('FLASK_PORT', '10000'))

