import sqlite3
from contextlib import contextmanager


@contextmanager
def open_db(file_name: str):
    conn = sqlite3.connect(file_name)
    try:
        yield conn.cursor()
    finally:
        conn.commit()
        conn.close()
