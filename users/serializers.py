from django.contrib.auth.models import User
from rest_framework import serializers


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации пользователя через DRF.
    """
    password = serializers.CharField(write_only=True, help_text="Пароль пользователя")

    class Meta:
        model = User
        fields = ("id", "username", "password", "email")

    def create(self, validated_data):
        """Создает нового пользователя с хешированным паролем"""

        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data.get("email", "")
        )
        return user
