#!/usr/bin/env bash
# exit on error
set -o errexit

# Установка зависимостей
pip install --upgrade pip
pip install -r requirements.txt

# Создание необходимых директорий
mkdir -p instance

# Установка переменных окружения
export FLASK_APP=wsgi.py
export FLASK_ENV=production

# Инициализация базы данных
python3 -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"

# Применение миграций
flask db upgrade

# Добавление начальных данных
python3 add_green_zones.py
