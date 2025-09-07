from collections.abc import Generator
from dataclasses import astuple, fields

from psycopg.connection import Connection


alias = {"created_at": "created", "updated_at": "modified"}


class PostgresSaver:
    def __init__(self, pg_conn: Connection):
        self.pg_conn = pg_conn

    def save_all_data(self, data: dict[str, Generator]) -> None:
        with self.pg_conn.cursor() as cur:
            for table, gen in data.items():
                for batch in gen:
                    if not batch:
                        continue
                    sample = batch[0]
                    cols_raw = [f.name for f in fields(sample)]
                    cols = [alias.get(c, c) for c in cols_raw]
                    placeholders = ", ".join(["%s"] * len(cols))
                    col_list = ", ".join(cols)
                    query = (
                        f"INSERT INTO content.{table} ({col_list}) "
                        f"VALUES ({placeholders}) "
                        f"ON CONFLICT (id) DO NOTHING"
                    )
                    values = [astuple(item) for item in batch]
                    cur.executemany(query, values)
        self.pg_conn.commit()
