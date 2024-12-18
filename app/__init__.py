from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.models import User
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from app.main.routes import main_blueprint
    app.register_blueprint(main_blueprint)

    from app.auth.routes import auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.admin.routes import admin_blueprint
    app.register_blueprint(admin_blueprint)

    return app
