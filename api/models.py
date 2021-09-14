from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


def validate_phone_number(value):
    if len(value) != 11:
        raise ValidationError('전화번호는 11자리 입니다')

    if value.startswith('010'):
        raise ValidationError('010으로 시작하는 번호를 적어주세요')


class User(AbstractUser):

    """ User Model Definition """

    username = models.CharField(max_length=64, blank=True)
    birthday = models.DateField(blank=True, null=True)
    phone_number = models.CharField(verbose_name="휴대폰 번호", max_length=11, unique=True, validators=[validate_phone_number])

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


class Voice(TimeStampedModel):

    """ Voice Model to analyze and save pitches """

    # 목소리 음역대 저장
    max_pitch = models.CharField(max_length=2, blank=True, null=True)
    min_pitch = models.CharField(max_length=2, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='voices')


class File(TimeStampedModel):

    """ File Model to save voice files """

    filename = models.FileField(upload_to="voices", blank=False, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')


class Song(TimeStampedModel):

    """ Song Model to save songs with pitch and info """

    title = models.CharField(max_length=200, blank=False, null=False)
    max_pitch = models.CharField(max_length=2, blank=False, null=False)  # 음역대
    min_pitch = models.CharField(max_length=2, blank=False, null=False)
    singer = models.ForeignKey('Singer', on_delete=models.SET_NULL, null=True, related_name='songs')
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

    kor_name = models.CharField(max_length=100)
    eng_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_debut = models.DateField(null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.kor_name
