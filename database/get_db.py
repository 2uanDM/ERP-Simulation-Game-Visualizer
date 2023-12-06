import sqlite3
import os


def get_db() -> sqlite3.Connection:
    db_path = os.path.join(os.getcwd(), 'erp.db')
    if not os.path.exists(db_path):
        raise Exception(f"==>> The database file does not exist: {db_path}")
    conn = sqlite3.connect(db_path)
    return conn
