import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField("name", max_length=255)
    description = models.TextField("description", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"genre"  # fmt: skip
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class FilmWork(UUIDMixin, TimeStampedMixin):
    class FilmType(models.TextChoices):
        MOVIE = "movie"
        TV_SHOW = "tv_show"

    title = models.CharField("title", blank=False, max_length=255)
    description = models.TextField("description", blank=True)
    creation_date = models.DateField("creation_date", blank=False)
    rating = models.FloatField(
        "rating",
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
    )
    type = models.CharField("type", choices=FilmType.choices)  # type: ignore
    genres = models.ManyToManyField(Genre, through="GenreFilmWork")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"film_work"  # fmt: skip
        verbose_name = "Кинопроизведение"
        verbose_name_plural = "Кинопроизведения"


class GenreFilmWork(UUIDMixin):
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE)
    film_work = models.ForeignKey("FilmWork", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"  # fmt: skip
