from django.urls import path

from .views import TelegramWebhookView

app_name = "telegram_bot"

urlpatterns = [
    # URL для приема webhook от Telegram
    # <secret> используется для защиты эндпоинта
    path(
        "webhook/<str:secret>/",
        TelegramWebhookView.as_view(),
        name="webhook",
    ),
]
