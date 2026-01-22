from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Права доступа для Habit:

    - Владелец может создавать, изменять и удалять свои привычки.
    - Другие пользователи могут только читать (SAFE_METHODS).
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
