from app import create_app, db
from app.models import Tree, User
from datetime import datetime, timedelta
import random

app = create_app()

def add_trees():
    with app.app_context():
        # Удаляем существующие деревья
        Tree.query.delete()
        
        # Находим первого пользователя для привязки деревьев
        first_user = User.query.first()
        if not first_user:
            print("Сначала создайте пользователя!")
            return
        
        # Список тестовых деревьев
        tree_data = [
            {
                'species': 'oak',
                'latitude': 55.7558,
                'longitude': 37.6173,
                'description': 'Дерево в центральном парке',
                'status': 'mature'
            },
            {
                'species': 'maple',
                'latitude': 55.7620,
                'longitude': 37.6089,
                'description': 'Молодой клён на аллее',
                'status': 'young'
            },
            {
                'species': 'birch',
                'latitude': 55.7500,
                'longitude': 37.6250,
                'description': 'Берёза в школьном дворе',
                'status': 'healthy'
            },
            {
                'species': 'pine',
                'latitude': 55.7700,
                'longitude': 37.6300,
                'description': 'Сосна в лесопарковой зоне',
                'status': 'needs_care'
            },
            {
                'species': 'spruce',
                'latitude': 55.7450,
                'longitude': 37.6150,
                'description': 'Ель на территории университета',
                'status': 'mature'
            }
        ]
        
        # Создаем деревья
        trees = []
        for data in tree_data:
            tree = Tree(
                species=data['species'],
                latitude=data['latitude'],
                longitude=data['longitude'],
                description=data['description'],
                status=data['status'],
                planted_by=first_user.id,
                planting_date=datetime.utcnow() - timedelta(days=random.randint(30, 365))
            )
            trees.append(tree)
        
        # Добавляем деревья в сессию
        db.session.add_all(trees)
        
        # Сохраняем изменения
        db.session.commit()
        print("Тестовые деревья успешно добавлены!")

if __name__ == '__main__':
    add_trees()
