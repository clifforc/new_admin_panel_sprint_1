from django.contrib import admin
from .models import FilmWork, Genre, GenreFilmWork


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmWorkInline,)
