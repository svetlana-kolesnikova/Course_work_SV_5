# -----------------------------
# Настройки сервера
# -----------------------------
SERVER_USER=svps
SERVER_IP=158.160.4.254
REMOTE_DIR=/home/svps/Course_work_SV_5

# -----------------------------
# Локальные команды
# -----------------------------
.PHONY: install
install:
	@echo "Installing dependencies..."
	poetry install

.PHONY: migrate
migrate:
	@echo "Applying Django migrations..."
	poetry run python manage.py migrate

.PHONY: collectstatic
collectstatic:
	@echo "Collecting static files..."
	poetry run python manage.py collectstatic --noinput

.PHONY: up
up:
	@echo "Building and starting Docker containers..."
	docker-compose up -d --build

.PHONY: down
down:
	@echo "Stopping Docker containers..."
	docker-compose down

.PHONY: logs
logs:
	@echo "Following web logs..."
	docker-compose logs -f web

.PHONY: run
run:
	@echo "Starting Django locally (without Docker)..."
	poetry run gunicorn config.wsgi:application --bind 0.0.0.0:8000

.PHONY: celery
celery:
	@echo "Starting Celery worker..."
	poetry run celery -A config worker -l info

.PHONY: celery-beat
celery-beat:
	@echo "Starting Celery beat..."
	poetry run celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

# -----------------------------
# Локальный полный запуск одной командой
# -----------------------------
.PHONY: local
local: install migrate collectstatic up
	@echo "Starting Celery worker and beat in background..."
	# Celery worker
	poetry run celery -A config worker -l info --detach
	# Celery beat
	poetry run celery -A config beat -l info --detach --scheduler django_celery_beat.schedulers:DatabaseScheduler
	@echo "Project is ready! Access at http://localhost:8000"

# -----------------------------
# Деплой на удалённый сервер
# -----------------------------
.PHONY: deploy
deploy:
	@echo "Deploying to remote server..."
	@ssh -i ~/.ssh/id_ed25519 $(SERVER_USER)@$(SERVER_IP) "\
		cd $(REMOTE_DIR) && \
		git pull origin develop && \
		docker-compose pull && \
		docker-compose up -d --build \
	"
