from django.contrib import admin
from . import models


@admin.register(models.Voice)
class VoiceAdmin(admin.ModelAdmin):
    pass


@admin.register(models.File)
class FileAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Song)
class SongAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "max_pitch",
        "singers",
        "genres",
    )

    def singers(self, obj):
        result = []
        for singer in obj.singer.all():
            if singer:
                result.append(singer.name)
        if result:
            return ", ".join(result)
        else:
            return "저장 필요"

    def genres(self, obj):
        result = []
        for genre in obj.genre.all():
            if genre:
                result.append(genre.name)
        if result:
            return ", ".join(result)
        else:
            return "저장 필요"


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Singer)
class SingerAdmin(admin.ModelAdmin):
    pass
