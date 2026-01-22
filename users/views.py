from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserRegistrationSerializer


class RegisterView(generics.CreateAPIView):
    """
    Эндпоинт регистрации нового пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    """
    Эндпоинт авторизации пользователя.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {"detail": "Неверные учетные данные"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


class LogoutView(APIView):
    """
    Эндпоинт выхода пользователя.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Удаляет текущий токен пользователя, делая его недействительным"""

        if request.auth:
            request.auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
