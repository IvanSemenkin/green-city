from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class GreenZone(db.Model):
    __tablename__ = 'green_zones'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    area = db.Column(db.Float)  # площадь в гектарах
    type = db.Column(db.String(100))  # тип зеленой зоны (парк, сквер, лесопарк и т.д.)
    district = db.Column(db.String(100))  # район Пензенской области
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'area': self.area,
            'type': self.type,
            'district': self.district
        }

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200))
    event_type = db.Column(db.String(50), nullable=False, default='other')  # тип мероприятия
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    EVENT_TYPES = {
        'subbotnik': 'Субботник',
        'tree_planting': 'Посадка деревьев',
        'eco_lecture': 'Эко-лекция',
        'cleanup': 'Уборка территории',
        'recycling': 'Сбор вторсырья',
        'eco_festival': 'Эко-фестиваль',
        'workshop': 'Мастер-класс',
        'other': 'Другое'
    }

    @staticmethod
    def get_event_types():
        return Event.EVENT_TYPES

class Tree(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String(100), nullable=False)
    planting_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    planted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(50), default='healthy')
    description = db.Column(db.Text)
    
    # Связь с пользователем
    planter = db.relationship('User', backref=db.backref('planted_trees', lazy=True))
    
    TREE_STATUSES = {
        'healthy': 'Здоровое',
        'needs_care': 'Требует ухода',
        'young': 'Молодое',
        'mature': 'Взрослое'
    }
    
    TREE_SPECIES = {
        'oak': 'Дуб',
        'maple': 'Клён',
        'birch': 'Берёза',
        'pine': 'Сосна',
        'spruce': 'Ель',
        'apple': 'Яблоня',
        'cherry': 'Вишня',
        'other': 'Другое'
    }
    
    def __repr__(self):
        return f'<Tree {self.species} planted on {self.planting_date}>'

# Таблица связи пользователей и челленджей
user_challenges = db.Table('user_challenges',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('challenge_id', db.Integer, db.ForeignKey('eco_challenge.id'), primary_key=True)
)

class EcoChallenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    
    # Связь с пользователями
    participants = db.relationship('User', 
                                 secondary=user_challenges,
                                 lazy='subquery',
                                 backref=db.backref('challenges', lazy=True))
    
    def __repr__(self):
        return f'<EcoChallenge {self.title}>'

class EcoTip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    points = db.Column(db.Integer, default=0)
    
    CATEGORIES = {
        'waste': 'Управление отходами',
        'energy': 'Энергосбережение', 
        'water': 'Водосбережение',
        'transport': 'Экологичный транспорт',
        'food': 'Устойчивое питание',
        'consumption': 'Осознанное потребление'
    }
    
    DIFFICULTY_LEVELS = {
        'easy': 'Легко',
        'medium': 'Средне',
        'hard': 'Сложно'
    }
    
    def __repr__(self):
        return f'<EcoTip {self.title}>'
