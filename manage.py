#!/usr/bin/env python3
import os
import sys
import click
from flask.cli import FlaskGroup

# Добавляем путь к приложению в PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models import User

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command('create_admin')
@click.argument('username')
@click.argument('email')
@click.argument('password')
def create_admin(username, email, password):
    """Создание администратора"""
    with app.app_context():
        # Проверяем существование пользователя
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        
        if existing_user:
            click.echo(f'Пользователь с именем {username} или email {email} уже существует.')
            return
        
        # Создаем нового пользователя с правами администратора
        new_admin = User(
            username=username, 
            email=email, 
            is_admin=True
        )
        new_admin.set_password(password)
        
        try:
            db.session.add(new_admin)
            db.session.commit()
            click.echo(f'Администратор {username} успешно создан!')
        except Exception as e:
            db.session.rollback()
            click.echo(f'Ошибка при создании администратора: {str(e)}')

if __name__ == '__main__':
    cli()
