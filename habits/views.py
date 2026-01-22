from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination

from habits.models import Habit
from habits.permissions import IsOwnerOrReadOnly
from habits.serializers import HabitSerializer


class HabitPagination(PageNumberPagination):
    """
    Пагинация привычек — 5 элементов на страницу.
    """
    page_size = 5


class HabitListCreateView(generics.ListCreateAPIView):
    """
    Список и создание привычек текущего пользователя.
    """
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user).order_by("time")


class HabitRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Просмотр, редактирование и удаление конкретной привычки.
    """
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Habit.objects.all()


class PublicHabitListView(generics.ListAPIView):
    """
    Список публичных привычек.
    """
    serializer_class = HabitSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(is_public=True).order_by("time")
