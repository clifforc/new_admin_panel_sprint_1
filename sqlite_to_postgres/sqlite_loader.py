from collections.abc import Generator
from sqlite3 import Connection, Cursor, Row

BATCH_SIZE = 100


class SQLiteLoader:
    def __init__(self, connection: Connection):
        self.connection = connection

    def load_movies(self):
        pass

    def _extract_data(self, sqlite_cursor: Cursor, table: str) -> Generator[list[Row]]:
        sqlite_cursor.execute(f"SELECT * FROM {table}")
        while results := sqlite_cursor.fetchmany(BATCH_SIZE):
            yield results
