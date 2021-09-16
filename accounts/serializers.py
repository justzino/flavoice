from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    # password 를 serializer 로 보여주는 것 방지
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone_number",
            "birthday",
            "password",  # password 입력 받기 위해
        )

        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.get("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
