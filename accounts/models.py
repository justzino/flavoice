from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


def validate_phone_number(value):
    if len(value) != 11:
        raise ValidationError('전화번호는 11자리 입니다')

    if not value.startswith('010'):
        raise ValidationError('010으로 시작하는 번호를 적어주세요')


GENDER_SELECTION = [
    ('M', 'M'),
    ('F', 'F'),
]


class CustomUser(AbstractUser):

    """ User Model Definition """

    username = models.CharField(blank=True, null=True, max_length=150)
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(verbose_name="휴대폰 번호", max_length=11, blank=True, null=True, validators=[validate_phone_number])
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_SELECTION)

    USERNAME_FIELD = "email"  # 로그인 email 로
    REQUIRED_FIELDS = []

    objects = CustomUserManager()  # username 안받으려고 manager 만듬

    def __str__(self):
        return self.email
