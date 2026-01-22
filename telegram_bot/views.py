import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from telegram_bot.models import TelegramProfile


class TelegramWebhookView(APIView):
    """
    Vievs для Telegram.
    """
    permission_classes = [AllowAny]

    def post(self, request, secret):
        """Обработка POST-запроса от Telegram"""

        # 1. Проверка секретного ключа
        if secret != settings.TELEGRAM_WEBHOOK_SECRET:
            return HttpResponseForbidden("Forbidden")

        message = request.data.get("message", {})
        text = message.get("text", "")
        chat_id = message.get("chat", {}).get("id")

        # 2. Игнорируем все, кроме команды /start
        if not text.startswith("/start") or not chat_id:
            return Response(status=200)

        parts = text.split()
        if len(parts) != 2:
            self._send_message(chat_id, "Неверная команда. Используйте /start <username>")
            return Response({"detail": "Неверная команда"}, status=400)

        username = parts[1]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self._send_message(chat_id, f"Пользователь {username} не найден")
            return Response({"detail": "Пользователь не найден"}, status=404)

        # 3. Привязка chat_id к пользователю
        TelegramProfile.objects.update_or_create(
            user=user,
            defaults={"chat_id": chat_id},
        )

        # 4. Отправка подтверждения в Telegram
        self._send_message(chat_id, f"Привет, {username}! Telegram успешно привязан.")

        return Response({"detail": "Telegram успешно привязан"})

    def _send_message(self, chat_id: int, text: str) -> None:
        """Отправка сообщения пользователю в Telegram через API"""

        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        try:
            requests.post(url, json=payload, timeout=5)
        except requests.RequestException:
            pass
