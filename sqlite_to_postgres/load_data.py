import os
import sqlite3

import psycopg
from dotenv import load_dotenv
from psycopg import ClientCursor
from psycopg.rows import dict_row

from sqlite_to_postgres.postgres_saver import PostgresSaver
from sqlite_to_postgres.sqlite_loader import SQLiteLoader
from sqlite_to_postgres.tests.check_consistency import test_transfer
from sqlite_to_postgres.utills import open_db


load_dotenv()


def load_from_sqlite(sqlite_cursor: sqlite3.Cursor, pg_conn: psycopg.Connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(sqlite_cursor)

    data = sqlite_loader.load_movies()
    postgres_saver.save_all_data(data)


if __name__ == "__main__":
    dsl = {
        "dbname": os.environ.get("DB_NAME"),
        "user": os.environ.get("DB_USER"),
        "password": os.environ.get("DB_PASSWORD"),
        "host": os.environ.get("DB_HOST", "127.0.0.1"),
        "port": os.environ.get("DB_PORT", 5432),
    }
    with (
        open_db(file_name="db.sqlite") as sqlite_cur,
        psycopg.connect(
            **dsl, row_factory=dict_row, cursor_factory=ClientCursor
        ) as pg_conn,
    ):
        load_from_sqlite(sqlite_cur, pg_conn)
        test_transfer(sqlite_cur, pg_conn)
