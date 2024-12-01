from app import create_app, db
from app.models import User

app = create_app()

def set_admin():
    with app.app_context():
        # Находим пользователя по имени
        user = User.query.filter_by(username='Иван').first()
        
        if user:
            # Устанавливаем права администратора
            user.is_admin = True
            db.session.commit()
            print(f"Пользователь {user.username} теперь администратор!")
        else:
            print("Пользователь с именем 'Иван' не найден. Сначала зарегистрируйтесь.")

if __name__ == '__main__':
    set_admin()
