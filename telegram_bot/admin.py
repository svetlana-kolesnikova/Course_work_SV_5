from django.contrib import admin

from telegram_bot.models import TelegramProfile


@admin.register(TelegramProfile)
class TelegramProfileAdmin(admin.ModelAdmin):
    """Админка для профиля в Телеграм"""
    list_display = ("user", "chat_id")
    search_fields = ("user__username", "chat_id")
    readonly_fields = ("chat_id",)
