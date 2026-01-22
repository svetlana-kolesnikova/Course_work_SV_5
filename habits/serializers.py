from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Habit для DRF.
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    last_notified = serializers.DateField(read_only=True)

    class Meta:
        model = Habit
        fields = "__all__"

    def validate(self, data):
        """
        Проверяет валидаторы модели перед сохранением через API.
        """
        habit = Habit(**data)
        habit.clean()
        return data
