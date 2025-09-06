import uuid
from django.db import models


class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("name", max_length=255)
    description = models.TextField("description", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"genre"  # fmt: skip
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class FilmWork(models.Model):
    class FilmType(models.TextChoices):
        MOVIE = "movie"
        TV_SHOW = "tv_show"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField("title", blank=False, max_length=255)
    description = models.TextField("description", blank=True)
    creation_date = models.DateField("creation_date", blank=False)
    rating = models.FloatField("rating", blank=True)
    type = models.CharField("type", choices=FilmType.choices)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"film_work"  # fmt: skip
        verbose_name = "Кинопроизведение"
        verbose_name_plural = "Кинопроизведения"
