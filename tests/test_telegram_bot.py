import pytest
from django.conf import settings

from telegram_bot.models import TelegramProfile


@pytest.mark.django_db
def test_telegram_webhook_binding(api_client, create_user, mock_telegram_send):
    """Привязка Telegram профиля через вебхук"""
    user = create_user(username="tguser")
    settings.TELEGRAM_WEBHOOK_SECRET = "supersecret"
    payload = {"message": {"text": f"/start {user.username}", "chat": {"id": 12345}}}

    response = api_client.post("/api/telegram/webhook/supersecret/", payload, format="json")
    assert response.status_code == 200
    profile = TelegramProfile.objects.get(user=user)
    assert profile.chat_id == 12345
