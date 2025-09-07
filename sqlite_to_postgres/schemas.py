from dataclasses import dataclass
from datetime import datetime, date
from enum import StrEnum
from uuid import UUID


@dataclass
class BaseUUID:
    id: UUID

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = UUID(self.id)


@dataclass
class BaseTimeStamped:
    created_at: datetime
    updated_at: datetime


class FilmType(StrEnum):
    MOVIE = "movie"
    TV_SHOW = "tv_show"


@dataclass
class FilmWork(BaseUUID, BaseTimeStamped):
    title: str
    rating: float
    type: FilmType
    file_path: str | None = None
    description: str | None = None
    creation_date: date | None = None


@dataclass(slots=True)
class Person(BaseUUID, BaseTimeStamped):
    full_name: str


@dataclass(slots=True)
class Genre(BaseUUID, BaseTimeStamped):
    name: str
    description: str | None = None


@dataclass(slots=True)
class PersonFilmWork(BaseUUID):
    person_id: UUID
    film_work_id: UUID
    role: str
    created_at: datetime


@dataclass(slots=True)
class GenreFilmWork(BaseUUID):
    genre_id: UUID
    film_work_id: UUID
    created_at: datetime
