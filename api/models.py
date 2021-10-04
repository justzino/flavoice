from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    """ Time Stamped Model """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Voice(TimeStampedModel):
    """ Voice Model to analyze and save pitches """

    # 목소리 음역대 저장
    max_pitch = models.IntegerField(default=0)
    min_pitch = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='voices')


class File(TimeStampedModel):
    """ File Model to save voice files """

    filename = models.FileField(upload_to="voices", blank=False, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='files')


class Song(TimeStampedModel):
    """ Song Model to save songs with pitch and info """

    title = models.CharField(max_length=200, blank=False, null=False)
    max_pitch = models.CharField(max_length=5, blank=False, null=False)  # 음역대
    min_pitch = models.CharField(max_length=5, blank=True, null=True)
    singer = models.ManyToManyField('Singer', related_name='songs')
    genre = models.ManyToManyField('Genre', related_name='songs', help_text='Select a genre for this song')

    def __str__(self):
        """String for representing the Model object."""
        return self.title


class Genre(TimeStampedModel):
    """ Genre Model """

    name = models.CharField(max_length=200, help_text='Enter a song genre (e.g. Hip-Hop)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Singer(models.Model):
    """ Singer Model """

    name = models.CharField(max_length=100)
    date_of_debut = models.DateField(null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.name
