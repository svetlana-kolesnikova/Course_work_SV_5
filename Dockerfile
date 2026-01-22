# Dockerfile
FROM python:3.13-slim

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

WORKDIR /app

# Копируем только файлы зависимостей для кэширования слоёв
COPY pyproject.toml poetry.lock* /app/

# Устанавливаем зависимости проекта
RUN poetry install --no-root

# Копируем весь проект
COPY . /app

# Открываем порт приложения
EXPOSE 8000

# Команда запуска Django через Gunicorn
CMD ["poetry", "run", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
