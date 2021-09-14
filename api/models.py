from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    """ User Model Definition """

    username = models.CharField(max_length=64, blank=True)
    birthday = models.DateField(blank=True, null=True)
    phone_number = models.CharField(verbose_name="휴대폰 번호", max_length=11, unique=True)

    USERNAME_FIELD = "phone_number"  # 로그인 phone_number 로
    REQUIRED_FIELDS = ["username", "birthday"]

    def __str__(self):
        return self.username


class TimeStampedModel(models.Model):

    """ Time Stamped Model """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Song(TimeStampedModel):

    """ Song Model """

    # 음역대
    PITCH_CHOICES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    title = models.CharField(max_length=200, blank=False, null=False)
    max_pitch = models.CharField(choices=PITCH_CHOICES, max_length=2, blank=False, null=False)
    min_pitch = models.CharField(choices=PITCH_CHOICES, max_length=2, blank=False, null=False)
    file = models.FileField(upload_to="songs", on_delete=models.SET_NULL, null=True)
    singer = models.ForeignKey('Singer', on_delete=models.SET_NULL, null=True)
    Genre = models.ManyToManyField('Genre', help_text='Select a genre for this song')

    def __str__(self):
        """String for representing the Model object."""
        return self.title


class Voice(TimeStampedModel):

    """ Voice Model """

    # 음역대
    PITCH_CHOICES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    max_pitch = models.CharField(choices=PITCH_CHOICES, max_length=2, blank=False, null=False)
    min_pitch = models.CharField(choices=PITCH_CHOICES, max_length=2, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='songs')


class Genre(TimeStampedModel):

    """ Model representing a song genre. """

    name = models.CharField(max_length=200, help_text='Enter a song genre (e.g. Hip-Hop)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Singer(models.Model):

    """ Model representing a Singer. """

    kor_name = models.CharField(max_length=100)
    eng_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_debut = models.DateField(null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.kor_name

