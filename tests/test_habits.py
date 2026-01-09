import pytest

from habits.models import Habit


@pytest.mark.django_db
def test_create_habit(authenticated_client):
    """Создание полезной привычки через API"""
    client, user = authenticated_client
    data = {
        "action": "Утренняя гимнастика",
        "place": "Дом",
        "time": "07:00",
        "is_pleasant": False,
        "reward": "Смузи",
        "frequency": 1,
        "duration": 60,
        "is_public": True
    }
    response = client.post("/api/habits/", data)
    assert response.status_code == 201
    habit = Habit.objects.get(user=user, action="Утренняя гимнастика")
    assert habit.reward == "Смузи"


@pytest.mark.django_db
def test_list_public_habits(habit_factory, authenticated_client):
    """Получение списка публичных привычек"""
    habit_factory()
    client, _ = authenticated_client
    response = client.get("/api/habits/public/")
    assert response.status_code == 200
    assert len(response.data["results"]) >= 1
