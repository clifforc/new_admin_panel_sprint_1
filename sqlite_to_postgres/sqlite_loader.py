from collections.abc import Generator
from sqlite3 import Cursor, Row

from sqlite_to_postgres.schemas import (
    FilmWork,
    Genre,
    GenreFilmWork,
    Person,
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
    def __init__(self, sqlite_cursor: Cursor):
        self.sqlite_cursor = sqlite_cursor
        self.sqlite_cursor.row_factory = Row

    def load_movies(self) -> dict[str, Generator[list[object], None, None]]:
        movies: dict[str, Generator[list[object], None, None]] = {}
        for table, model in TABLE_MODEL_MAP.items():
            movies[table] = self._transform_data(
                self.sqlite_cursor, table, model
            )
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
