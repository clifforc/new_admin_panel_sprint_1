from psycopg.connection import Connection


class PostgresSaver:
    def __init__(self, pg_conn: Connection):
        self.pg_conn = pg_conn

    def save_all_data(self, data):
        pass
