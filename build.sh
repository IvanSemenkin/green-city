#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Инициализация базы данных
python3 -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"

# Применение миграций
flask db upgrade

# Добавление зеленых зон
python3 add_green_zones.py
