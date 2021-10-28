from dj_rest_auth.registration.serializers import RegisterSerializer
from django.db import transaction
from rest_framework import serializers

from accounts.models import CustomUser
from accounts.models import GENDER_SELECTION


class CustomRegisterSerializer(RegisterSerializer):
    phone_number = serializers.CharField(max_length=11)
    birthday = serializers.DateField()
    gender = serializers.ChoiceField(choices=GENDER_SELECTION)

    # Define transaction.atomic to rollback the save operation in case of error
    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.phone_number = self.data.get('phone_number')
        user.birthday = self.data.get('birthday')
        user.gender = self.data.get('gender')
        user.save()
        return user


class CustomUserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'pk',
            'email',
            'phone_number',
            'gender',
        )
        read_only_fields = ('pk', 'email', 'phone_number',)