from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Habit(models.Model):
    """
    Модель привычки для трекера атомных привычек.

    Полезные привычки:
        - имеют вознаграждение или связанную приятную привычку
        - не могут иметь одновременно reward и related_habit

    Приятные привычки:
        - используются как вознаграждение для полезной привычки
        - не могут иметь reward или related_habit

    Поля:
        user: пользователь, создатель привычки
        place: место, где выполняется привычка
        time: время выполнения привычки
        action: описание действия привычки
        is_pleasant: признак приятной привычки
        related_habit: связанная приятная привычка
        frequency: периодичность выполнения (в днях)
        reward: вознаграждение за полезную привычку
        duration: время на выполнение (секунды)
        is_public: признак публичности привычки
        last_notified: дата последнего уведомления
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
        help_text="Пользователь, создавший привычку",
    )

    place = models.CharField(
        max_length=255,
        help_text="Место, где нужно выполнять привычку"
    )
    time = models.TimeField(
        help_text="Время, когда необходимо выполнять привычку"
    )
    action = models.CharField(
        max_length=255,
        help_text="Действие, которое представляет привычку"
    )

    is_pleasant = models.BooleanField(
        default=False,
        help_text="Признак приятной привычки"
    )

    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="related_to",
        help_text="Связанная приятная привычка для полезной привычки"
    )

    frequency = models.PositiveIntegerField(
        default=1,
        help_text="Периодичность выполнения привычки в днях (от 1 до 7)"
    )

    reward = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Вознаграждение за выполнение полезной привычки"
    )

    duration = models.PositiveIntegerField(
        help_text="Время выполнения привычки в секундах (≤ 120)"
    )

    is_public = models.BooleanField(
        default=False,
        help_text="Привычка доступна в публичном списке"
    )

    last_notified = models.DateField(
        null=True,
        blank=True,
        help_text="Дата последнего уведомления о привычке"
    )

    class Meta:
        ordering = ["time"]
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def clean(self):
        """
        Валидаторы модели Habit
        """
        super().clean()

        if self.duration > 120:
            raise ValidationError("Время выполнения не может превышать 120 секунд")

        if not 1 <= self.frequency <= 7:
            raise ValidationError("Периодичность должна быть от 1 до 7 дней")

        if self.is_pleasant:
            if self.reward:
                raise ValidationError("Приятная привычка не может иметь вознаграждение")
            if self.related_habit:
                raise ValidationError("Приятная привычка не может иметь связанную привычку")
        else:
            if not self.reward and not self.related_habit:
                raise ValidationError(
                    "Полезная привычка должна иметь вознаграждение "
                    "или связанную приятную привычку"
                )
            if self.reward and self.related_habit:
                raise ValidationError(
                    "Полезная привычка не может иметь одновременно вознаграждение и связанную привычку"
                )

        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной")

    def __str__(self):
        return f"{self.action} ({self.user})"
