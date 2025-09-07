from collections.abc import Generator
from sqlite3 import Connection, Cursor, Row

from sqlite_to_postgres.schemas import (
    FilmWork,
    Genre,
    Person,
    GenreFilmWork,
    PersonFilmWork,
)

BATCH_SIZE = 100
TABLE_MODEL_MAP = {
    "film_work": FilmWork,
    "genre": Genre,
    "person": Person,
    "genre_film_work": GenreFilmWork,
    "person_film_work": PersonFilmWork,
}


class SQLiteLoader:
    def __init__(self, connection: Connection):
        self.connection = connection
        self.connection.row_factory = Row

    def load_movies(self):
        movies: dict[str, list] = {}
        for table, model in TABLE_MODEL_MAP.items():
            gen = self._transform_data(self.connection.cursor(), table, model)
            movies[table] = [item for batch in gen for item in batch]
        return movies

    def _extract_data(
        self, sqlite_cursor: Cursor, table: str
    ) -> Generator[list[Row], None, None]:
        sqlite_cursor.execute(f"SELECT * FROM {table}")
        while results := sqlite_cursor.fetchmany(BATCH_SIZE):
            yield results

    def _transform_data[T](
        self, sqlite_cursor: Cursor, table: str, model: T
    ) -> Generator[list[T], None, None]:
        for batch in self._extract_data(sqlite_cursor, table):
            yield [model(**dict(row)) for row in batch]
