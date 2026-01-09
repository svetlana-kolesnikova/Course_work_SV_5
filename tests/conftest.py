import os
from datetime import time
from unittest.mock import patch

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from habits.models import Habit
from telegram_bot.models import TelegramProfile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


@pytest.fixture
def api_client():
    """
    Фикстура для DRF APIClient.
    Используется для отправки запросов к эндпоинтам.
    """
    return APIClient()


@pytest.fixture
def create_user():
    """Создает нового пользователя с уникальным username для тестов"""
    counter = 0

    def _create(username=None, password="password", email=None):
        nonlocal counter
        counter += 1
        username = username or f"testuser{counter}"
        return User.objects.create_user(
            username=username,
            password=password,
            email=email or f"{username}@example.com"
        )
    return _create


@pytest.fixture
def authenticated_client(api_client, create_user):
    """
    Фикстура для авторизованного клиента.
    Создает пользователя и логинит его в DRF APIClient.
    """
    user = create_user()
    api_client.force_authenticate(user=user)
    return api_client, user


@pytest.fixture
def habit_factory(create_user):
    """
    Фабрика для создания привычек.
    """
    def _create(user=None, **kwargs):
        user = user or create_user()
        defaults = {
            "action": "Тест действие",
            "place": "Дом",
            "time": time(hour=9, minute=0),
            "is_pleasant": False,
            "frequency": 1,
            "reward": "Кофе",
            "duration": 60,
            "is_public": True,
        }
        defaults.update(kwargs)
        return Habit.objects.create(user=user, **defaults)
    return _create


@pytest.fixture
def telegram_profile_factory(create_user):
    """
    Фабрика для создания TelegramProfile.
    """
    def _create(user=None, chat_id=12345):
        user = user or create_user()
        return TelegramProfile.objects.create(user=user, chat_id=chat_id)
    return _create


@pytest.fixture
def mock_telegram_send(monkeypatch):
    """
    Фикстура для мокирования отправки сообщений в Telegram.
    Подменяет requests.post на мок.
    """
    with patch("telegram_bot.services.requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        yield mock_post
