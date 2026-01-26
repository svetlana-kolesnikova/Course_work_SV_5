# Atomic Habits Tracker API


Проект реализует трекер атомных привычек с возможностью уведомлений через Telegram, 
управление публичными и личными привычками, а также регистрацию и аутентификацию пользователей.

---

## Стек технологий

- Python 3.13+
- Poetry
- Django 5
- Django REST Framework
- drf-spectacular (OpenAPI / Swagger / ReDoc)
- PostgreSQL
- Redis
- Celery
- django-celery-beat
- django-cors-headers
- psycopg2
- python-dotenv
- pytest, pytest-django (для тестирования)
- coverage (покрытие тестами)
- black, isort, flake8, mypy (линтинг и проверка типов)
- Docker, Docker Compose
- GitHub Actions (CI/CD)

---

## Возможности проекта

- Регистрация и авторизация пользователей
- API CRUD для привычек
- Публичные и личные привычки
- Валидация логики привычек (pleasant, reward, related_habit)
- Уведомления через Telegram по расписанию (Celery + Redis)
- Пагинация API (5 элементов на страницу)
- Swagger/OpenAPI документация
- Полное покрытие кода тестами (pytest, pytest-django)
- Автоматизированный деплой на удалённый сервер через GitHub Actions

---

## Установка и запуск (локально, без Docker)

### 1. Клонировать проект
```bash
git clone https://github.com/svetlana-kolesnikova/Course_work_SV_5
cd course-work-sv-5
```

### 2. Настроить переменные окружения
Скопировать файл [.env_sample](.env_sample) и заполнить переменные:
```bash
cp .env_sample .env
```
Заполнить необходимые переменные в .env:

Django: DJANGO_SECRET_KEY, DEBUG, ALLOWED_HOSTS

PostgreSQL: POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT

Redis: REDIS_URL

Telegram: TELEGRAM_BOT_TOKEN, TELEGRAM_WEBHOOK_SECRET

⚠️ Для локального запуска PostgreSQL и Redis должны быть установлены и запущены.


### 3. Запуск проекта одной командой
```bash
sudo docker compose down && \
sudo docker image prune -af && \
sudo docker volume prune -f && \
sudo docker compose up -d --build && \
sudo docker compose exec web poetry run python manage.py migrate && \
sudo docker compose exec web poetry run python manage.py collectstatic --noinput
```

После выполнения проект будет полностью развернут:
- База данных создана и мигрирована
- Статические файлы собраны
- Gunicorn сервер поднят
- Celery и Celery Beat запущены

---
## Загрузка учебных данных (фикстуры)

Проект содержит готовые фикстуры для быстрого заполнения базы данных пользователей, привычек и Telegram профилей.

### Шаги:

1. Убедитесь, что выполнены миграции:
```bash
python manage.py migrate
```
2. Загрузите пользователей:
```bash
python manage.py loaddata initial_users.json
```
3. Загрузите привычки:
```bash
python manage.py loaddata initial_habits.json
```
4. Загрузите Telegram профили:
```bash
python manage.py loaddata initial_telegram_profiles.json
```

⚠️ Обратите внимание: chat_id в фикстурах условные. 
Для тестов Telegram бота используйте реальные chat_id после привязки через /start < username >.

---

## Тестирование и покрытие кода

Запуск тестов:
```bash
pytest tests/
```

Генерация HTML-отчёта покрытия:
```bash
coverage run -m pytest
coverage html
```

Отчёт будет сохранён в папке:
```bash
htmlcov/index.html
```
📌 Папку htmlcov можно открыть в браузере.

---

## CI/CD через GitHub Actions

- Тесты и линтинг запускаются при push в develop и pull request.
- После успешных тестов проект автоматически деплоится на удалённый сервер через SSH.
- Используется единый workflow: .github/workflows/ci-cd.yml
- На сервере проект поднимается через Docker Compose с миграциями и сборкой статики.

---
## Приложения проекта

| Приложение     | Назначение                                         |
| -------------- | -------------------------------------------------- |
| `users`        | Модель пользователя, регистрация, авторизация      |
| `habits`       | CRUD для привычек, публичные и личные привычки     |
| `telegram_bot` | Привязка Telegram, отправка уведомлений через бота |
| `config`       | Настройки Django, Celery, URL маршруты             |

---

## Основные API эндпоинты

### Привычки

| Метод  | URL                   | Описание                     | Пример запроса                                          |
| ------ | --------------------- | ---------------------------- | ------------------------------------------------------- |
| GET    | `/api/habits/`        | Список привычек пользователя |                                                         |
| POST   | `/api/habits/`        | Создание новой привычки      | JSON с полями `action`, `place`, `time`, `reward` и др. |
| GET    | `/api/habits/public/` | Список публичных привычек    |                                                         |
| GET    | `/api/habits/<id>/`   | Просмотр привычки            |                                                         |
| PUT    | `/api/habits/<id>/`   | Обновление привычки          |                                                         |
| DELETE | `/api/habits/<id>/`   | Удаление привычки            |                                                         |


### Telegram

| Метод | URL                               | Описание                  | Пример запроса                                               |
| ----- | --------------------------------- | ------------------------- | ------------------------------------------------------------ |
| POST  | `/api/telegram/webhook/<secret>/` | Привязка Telegram профиля | `{"message":{"text":"/start username","chat":{"id":12345}}}` |


### Пользователи

| Метод | URL                    | Описание                        | Пример запроса                                                |
| ----- | ---------------------- | ------------------------------- | ------------------------------------------------------------- |
| POST  | `/api/users/register/` | Регистрация нового пользователя | `{"username":"user1","password":"pass","email":"a@test.com"}` |
| POST  | `/api/users/login/`    | Авторизация пользователя        | `{"username":"user1","password":"pass"}`                      |
| POST  | `/api/users/logout/`   | Выход пользователя              | (не требует тела запроса)                                     |

---

## API документация

Проект использует OpenAPI спецификацию и автодокументацию:

OpenAPI schema: http://127.0.0.1:8000/api/schema/

Swagger UI: http://127.0.0.1:8000/api/docs/swagger/

ReDoc: http://127.0.0.1:8000/api/docs/redoc/

---

## Postman

В репозитории присутствует Postman-коллекция со всеми API-запросами проекта.  
Коллекция полностью соответствует текущим API эндпоинтам 

[Course_work-5.postman_collection.json](Course_work-5.postman_collection.json)

📌 Её можно импортировать в Postman и использовать переменные окружения для localhost.

---

## Модели проекта

### Habit (habits.Habit)
- user — владелец привычки
- action — описание привычки
- place — место выполнения
- time — время выполнения
- is_pleasant — признак приятной привычки
- related_habit — связанная приятная привычка
- reward — вознаграждение за полезную привычку
- frequency — периодичность в днях
- duration — длительность в секундах
- is_public — публичная привычка
- last_notified — дата последнего уведомления

Валидации:

- Время выполнения ≤ 120 секунд
- Периодичность 1–7 дней
- Pleasant habit не может иметь reward и related_habit
- Полезная привычка должна иметь reward или related_habit, но не оба сразу

### TelegramProfile (telegram_bot.TelegramProfile)
- user — владелец профиля
- chat_id — идентификатор чата Telegram
- created_at — дата создания профиля

### User (django.contrib.auth.models.User)
- Стандартная модель пользователя Django
- Используется для привязки привычек и Telegram

---

## Тестирование проекта

### Фикстуры (tests/conftest.py):
- api_client — DRF APIClient
- create_user — создание пользователя
- authenticated_client — клиент с аутентификацией
- habit_factory — фабрика привычек
- telegram_profile_factory — фабрика Telegram профилей
- mock_telegram_send — мок Telegram API

### Примеры тестов:
- tests/test_habits.py — CRUD привычек, публичные привычки
- tests/telegram-bot.py — привязка Telegram через вебхук
- tests/users.py — регистрация, логин и получение токена

---

### Автор
Svetlana Kolesnikova
---
