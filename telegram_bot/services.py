import requests
from django.conf import settings


def send_telegram_message(chat_id: int, text: str) -> None:
    """
    Отправляет текстовое сообщение пользователю в Telegram.
    """
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка при отправке Telegram-сообщения: {e}")
