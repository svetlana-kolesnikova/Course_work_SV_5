from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from telegram_bot.services import send_telegram_message


@shared_task
def send_habit_reminders():
    """
    Задача Celery для отправки напоминаний о привычках через Telegram.

    Проверяет текущее время и выбирает привычки,
    которые должны быть выполнены сейчас.
    Отправляет сообщение пользователю и обновляет last_notified.
    """
    now = timezone.localtime()
    current_time = now.time()

    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute,
    )

    for habit in habits:
        telegram_profile = getattr(habit.user, "telegram_profile", None)
        if not telegram_profile:
            continue

        # проверка на last_notified
        if habit.last_notified:
            delta = (timezone.now().date() - habit.last_notified).days
            if delta < habit.frequency:
                continue

        message = (
            f"⏰ Напоминание!\n\n"
            f"⚡ Действие: {habit.action}\n"
            f"📍 Место: {habit.place}\n"
            f"🕒 Время: {habit.time.strftime('%H:%M')}"
        )

        send_telegram_message(
            chat_id=telegram_profile.chat_id,
            text=message,
        )

        habit.last_notified = now.date()
        habit.save(update_fields=["last_notified"])
