from django.contrib import admin

from .models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "created", "modified")
    search_fields = ("name",)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("full_name", "created", "modified")
    search_fields = ("full_name",)


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmWorkInline, PersonFilmWorkInline)

    list_display = (
        "title",
        "type",
        "creation_date",
        "rating",
        "created",
        "modified",
        "get_genres",
    )
    list_prefetch_related = ("genres",)

    def get_queryset(self, request):
        queryset = (
            super()
            .get_queryset(request)
            .prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ",".join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = "Жанры фильма"

    list_filter = ("type",)
    search_fields = ("title", "description", "id")
    autocomplete_fields = ("persons",)
