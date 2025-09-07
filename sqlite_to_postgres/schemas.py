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
    created: datetime
    modified: datetime


class FilmType(StrEnum):
    MOVIE = "movie"
    TV_SHOW = "tv_show"


@dataclass
class FilmWork(BaseUUID, BaseTimeStamped):
    title: str
    creation_date: date
    rating: float
    type: FilmType
    description: str | None = None

    def __post_init__(self):
        super().__post_init__()


@dataclass(slots=True)
class Person(BaseUUID, BaseTimeStamped):
    full_name: str

    def __post_init__(self):
        super().__post_init__()


@dataclass(slots=True)
class Genre(BaseUUID, BaseTimeStamped):
    name: str
    description: str | None = None

    def __post_init__(self):
        super().__post_init__()


@dataclass(slots=True)
class PersonFilmWork(BaseUUID):
    person_id: UUID
    film_work_id: UUID
    role: str
    created: datetime

    def __post_init__(self):
        super().__post_init__()


@dataclass(slots=True)
class GenreFilmWork(BaseUUID):
    genre_id: UUID
    film_work_id: UUID
    created: datetime

    def __post_init__(self):
        super().__post_init__()
