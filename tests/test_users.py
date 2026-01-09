import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
def test_user_registration(api_client, create_user):
    """Регистрация нового пользователя через API"""
    data = {"username": "newuser", "password": "Password123", "email": "a@test.com"}
    response = api_client.post("/api/users/register/", data)
    assert response.status_code == 201
    assert User.objects.filter(username="newuser").exists()


@pytest.mark.django_db
def test_user_login(api_client, create_user):
    """Логин пользователя и получение токена"""
    user = create_user(username="loginuser")
    user.set_password("Password123")
    user.save()
    response = api_client.post("/api/users/login/", {"username": "loginuser", "password": "Password123"})
    assert response.status_code == 200
    assert "token" in response.data
    token = response.data["token"]
    assert Token.objects.filter(key=token).exists()
