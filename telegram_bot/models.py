from django.conf import settings
from django.db import models


class TelegramProfile(models.Model):
    """
    Модель профиля Telegram для привязки к пользователю.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="telegram_profile",
        help_text="Пользователь, связанный с профилем Telegram"
    )

    chat_id = models.BigIntegerField(
        unique=True,
        verbose_name="Telegram chat ID",
        help_text="Уникальный идентификатор чата пользователя в Telegram"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Дата и время создания профиля"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Telegram профиль"
        verbose_name_plural = "Telegram профили"

    def __str__(self):
        """
        Строковое представление модели.
        """
        return f"{self.user.username} ({self.chat_id})"
