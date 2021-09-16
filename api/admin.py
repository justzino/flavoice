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
    pass


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Singer)
class SingerAdmin(admin.ModelAdmin):
    pass
