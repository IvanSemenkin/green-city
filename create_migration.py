from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import sys
import os

# Добавляем путь к проекту в sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Импортируем модели после инициализации db
from app.models import EcoChallenge

if __name__ == '__main__':
    with app.app_context():
        print("Creating migration...")
