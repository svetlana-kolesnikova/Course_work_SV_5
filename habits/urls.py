from django.urls import path

from habits.views import HabitListCreateView, HabitRetrieveUpdateDestroyView, PublicHabitListView

app_name = "habits"

urlpatterns = [
    path("", HabitListCreateView.as_view(), name="habit-list-create"),
    path("public/", PublicHabitListView.as_view(), name="habit-public-list"),
    path("<int:pk>/", HabitRetrieveUpdateDestroyView.as_view(), name="habit-detail"),
]
