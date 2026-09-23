import sqlite3
from config.settings import Config


def get_db_connection():
    """Создает и возвращает подключение к базе данных"""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

