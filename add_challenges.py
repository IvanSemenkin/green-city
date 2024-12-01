from app import create_app, db
from app.models import EcoChallenge
from datetime import datetime, timedelta

app = create_app()

def add_challenges():
    with app.app_context():
        # Удаляем существующие челленджи
        EcoChallenge.query.delete()
        
        # Создаем активный челлендж
        active_challenge = EcoChallenge(
            title="Зеленый город",
            description="Посади дерево и помоги городу стать экологичнее!",
            start_date=datetime.now() - timedelta(days=7),
            end_date=datetime.now() + timedelta(days=14),
            points=50
        )
        
        # Создаем предстоящий челлендж
        upcoming_challenge = EcoChallenge(
            title="Чистый берег",
            description="Присоединяйтесь к уборке прибрежной территории!",
            start_date=datetime.now() + timedelta(days=30),
            end_date=datetime.now() + timedelta(days=45),
            points=75
        )
        
        # Создаем завершенный челлендж
        completed_challenge = EcoChallenge(
            title="Раздельный сбор",
            description="Научись правильно сортировать мусор",
            start_date=datetime.now() - timedelta(days=45),
            end_date=datetime.now() - timedelta(days=30),
            points=25
        )
        
        # Добавляем челленджи в сессию
        db.session.add(active_challenge)
        db.session.add(upcoming_challenge)
        db.session.add(completed_challenge)
        
        # Сохраняем изменения
        db.session.commit()
        print("Челленджи успешно добавлены!")

if __name__ == '__main__':
    add_challenges()
