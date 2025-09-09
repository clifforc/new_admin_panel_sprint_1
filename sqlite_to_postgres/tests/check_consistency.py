import sqlite3
from datetime import datetime
from uuid import UUID

import psycopg

from sqlite_to_postgres.sqlite_loader import BATCH_SIZE, TABLE_MODEL_MAP


alias = {"created": "created_at", "modified": "updated_at"}


def normalize_record(s):
    if not isinstance(s, str):
        return s
    try:
        s = datetime.fromisoformat(s)
        return s
    except ValueError:
        try:
            s = UUID(s)
            return s
        except ValueError:
            return s


def test_transfer(sqlite_cursor: sqlite3.Cursor, pg_conn: psycopg.Connection):
    for table, model in TABLE_MODEL_MAP.items():
        pg_cursor = pg_conn.cursor()

        sqlite_cursor.execute(f"SELECT * FROM {table}")

        while batch := sqlite_cursor.fetchmany(BATCH_SIZE):
            original_row_batch = [
                {k: normalize_record(v) for k, v in dict(row).items()} for row in batch
            ]
            ids = [row["id"] for row in original_row_batch]

            pg_cursor.execute(f"SELECT * FROM {table} WHERE id = ANY(%s)", [ids])
            transferred_row_batch = [
                {alias.get(k, k): v for k, v in row.items()}
                for row in pg_cursor.fetchall()
            ]
            assert len(original_row_batch) == len(transferred_row_batch)
            assert original_row_batch == transferred_row_batch
