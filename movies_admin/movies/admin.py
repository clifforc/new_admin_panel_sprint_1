from django.contrib import admin
from .models import FilmWork, Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    pass
