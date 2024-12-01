#!/usr/bin/env bash
# exit on error
set -o errexit

# Установка зависимостей
pip install -r requirements.txt

# Создание необходимых директорий
mkdir -p instance

# Инициализация базы данных
export FLASK_APP=app.py
python3 -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"

# Применение миграций
flask db upgrade

# Добавление начальных данных
python3 add_green_zones.py
