import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(_("created"), auto_now_add=True)
    modified = models.DateTimeField(_("modified"), auto_now=True)

    class Meta:
        abstract = True


class FilmType(models.TextChoices):
    MOVIE = "movie", _("movie")
    TV_SHOW = "tv_show", _("tv_show")


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"genre"  # fmt: skip
        verbose_name = _("Жанр")
        verbose_name_plural = _("Жанры")
        ordering = ["-name"]
        indexes = [
            models.Index(fields=["name"], name="genre_name_idx"),
        ]


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_("full_name"), max_length=255, blank=False)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "content\".\"person"  # fmt: skip
        verbose_name = _("Персона")
        verbose_name_plural = _("Персоны")
        ordering = ["-full_name"]
        indexes = [
            models.Index(fields=["full_name"], name="person_full_name_idx"),
        ]


class FilmWork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_("title"), blank=False, max_length=255)
    description = models.TextField(_("description"), null=True, blank=True)
    creation_date = models.DateField(_("creation_date"), null=True, blank=True)
    rating = models.FloatField(
        _("rating"),
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
    )
    type = models.CharField(_("type"), choices=FilmType.choices)  # type: ignore
    file_path = models.TextField(_("file_path"), null=True, blank=True)
    genres = models.ManyToManyField(Genre, through="GenreFilmWork")
    persons = models.ManyToManyField(Person, through="PersonFilmWork")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"film_work"  # fmt: skip
        verbose_name = _("Кинопроизведение")
        verbose_name_plural = _("Кинопроизведения")
        ordering = ["-title"]
        indexes = [
            models.Index(
                fields=["creation_date"], name="film_work_creation_date_idx"
            ),
            models.Index(fields=["title"], name="film_work_title_idx"),
            models.Index(fields=["rating"], name="film_work_rating_idx"),
        ]


class PersonFilmWork(UUIDMixin):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE)
    role = models.CharField(_("role"), max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"  # fmt: skip

        constraints = [
            models.UniqueConstraint(
                fields=["person", "film_work", "role"],
                name="uq_person_film_role",
            )
        ]


class GenreFilmWork(UUIDMixin):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"  # fmt: skip

        constraints = [
            models.UniqueConstraint(
                fields=["genre", "film_work"],
                name="uk_genre_film",
            )
        ]
