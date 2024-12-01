#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models import GreenZone

def add_green_zones():
    green_zones_data = [
        # Пенза
        {
            "name": "Городской парк культуры и отдыха",
            "description": "Центральный парк Пензы с множеством аллей и зон отдыха",
            "latitude": 53.1952,
            "longitude": 45.0002,
            "area": 25.5,
            "type": "Городской парк",
            "district": "Пенза"
        },
        {
            "name": "Сквер Победы",
            "description": "Мемориальный сквер в честь победы в Великой Отечественной войне",
            "latitude": 53.1988,
            "longitude": 45.0089,
            "area": 3.2,
            "type": "Сквер",
            "district": "Пенза"
        },
        {
            "name": "Лесопарк Терновка",
            "description": "Большой лесной массив на окраине города",
            "latitude": 53.2256,
            "longitude": 44.9378,
            "area": 150.0,
            "type": "Лесопарк",
            "district": "Пенза"
        },
        {
            "name": "Детский парк Олимп",
            "description": "Парк с детскими площадками и аттракционами",
            "latitude": 53.1876,
            "longitude": 45.0156,
            "area": 5.7,
            "type": "Детский парк",
            "district": "Пенза"
        },
        {
            "name": "Парк имени Белинского",
            "description": "Исторический парк в центре города",
            "latitude": 53.1943,
            "longitude": 45.0045,
            "area": 12.3,
            "type": "Городской парк",
            "district": "Пенза"
        },
        # Заречный
        {
            "name": "Зона отдыха Заречный",
            "description": "Природная зона на берегу реки",
            "latitude": 53.2245,
            "longitude": 45.1567,
            "area": 45.0,
            "type": "Природная зона",
            "district": "Заречный"
        },
        # Другие районы
        {
            "name": "Бульвар Строителей",
            "description": "Благоустроенный бульвар с зеленой аллеей",
            "latitude": 53.1912,
            "longitude": 45.0234,
            "area": 2.5,
            "type": "Бульвар",
            "district": "Пенза"
        },
        # Новые зоны
        {
            "name": "Тропа здоровья",
            "description": "Оборудованная экологическая тропа для занятий спортом и активного отдыха",
            "latitude": 53.2034,
            "longitude": 44.9876,
            "area": 8.5,
            "type": "Природная зона",
            "district": "Пенза"
        },
        {
            "name": "Парк Белинского",
            "description": "Живописный парк с богатой историей и зеленым ландшафтом",
            "latitude": 53.1967,
            "longitude": 45.0123,
            "area": 15.6,
            "type": "Городской парк",
            "district": "Пенза"
        },
        {
            "name": "Олимпийская Аллея",
            "description": "Широкая аллея с современным благоустройством и спортивными площадками",
            "latitude": 53.2012,
            "longitude": 45.0067,
            "area": 4.2,
            "type": "Бульвар",
            "district": "Пенза"
        }
    ]

    app = create_app()
    with app.app_context():
        # Очищаем существующие записи
        GreenZone.query.delete()
        
        # Добавляем новые зоны
        for zone_data in green_zones_data:
            green_zone = GreenZone(**zone_data)
            db.session.add(green_zone)
        
        db.session.commit()
        print(f"Добавлено {len(green_zones_data)} зеленых зон")

if __name__ == "__main__":
    add_green_zones()
