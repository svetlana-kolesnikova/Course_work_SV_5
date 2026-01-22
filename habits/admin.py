from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """
    Админка для модели Habit.
    """
    def reward_or_related(self, obj):
        return obj.reward or (obj.related_habit.action if obj.related_habit else "-")

    reward_or_related.short_description = "Reward / Related Habit"

    list_display = (
        "id",
        "user",
        "action",
        "place",
        "time",
        "is_pleasant",
        "frequency",
        "reward",
        "is_public",
        "last_notified",
    )
    list_filter = ("user", "is_public", "is_pleasant")
    search_fields = ("action", "place")
    ordering = ("time",)
    readonly_fields = ("last_notified",)
