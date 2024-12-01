# 🌱 Green City - Эко-портал города

Веб-платформа для развития экологической культуры и озеленения города.

## Функциональность

- Карта зеленых зон и парков
- Календарь эко-мероприятий
- Советы по экологичному образу жизни
- Система учета посаженных деревьев
- Эко-челленджи для жителей

## Технический стек

- Backend: Python Flask
- Frontend: React
- Database: PostgreSQL
- Authentication: JWT + Flask-Login

## Установка и запуск

1. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Настройте переменные окружения:
```bash
cp .env.example .env
# Отредактируйте .env файл
```

4. Запустите приложение:
```bash
flask run
```
