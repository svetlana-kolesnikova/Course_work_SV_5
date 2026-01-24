# Dockerfile
FROM python:3.13-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry без кэша
RUN pip install --no-cache-dir poetry

# Отключаем создание виртуальных окружений внутри Poetry
RUN poetry config virtualenvs.create false

# Рабочая директория
WORKDIR /app

# Копируем файлы зависимостей для кэширования слоёв
COPY pyproject.toml poetry.lock /app/

# Устанавливаем зависимости проекта
RUN poetry install --no-root --no-interaction --no-ansi

# Копируем весь проект
COPY . /app

# Создаём директорию для collectstatic
RUN mkdir -p /app/staticfiles

# Открываем порт приложения
EXPOSE 8000

# Команда запуска Django через Gunicorn с 3 воркерами
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--log-level", "info"]
