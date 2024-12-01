from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse
from app import db
from app.auth import auth_blueprint
from app.models import User
import re

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').lower()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Пожалуйста, заполните все поля', 'danger')
            return redirect(url_for('auth.login'))
        
        if not is_valid_email(email):
            flash('Пожалуйста, введите корректный email', 'danger')
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(email=email).first()
        
        if user is None or not user.check_password(password):
            flash('Неверный email или пароль', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=bool(request.form.get('remember')))
        flash('Вы успешно вошли в систему!', 'success')
        
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Вход')

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password', '')
        password2 = request.form.get('password2', '')
        
        if not username or not email or not password or not password2:
            flash('Пожалуйста, заполните все поля', 'danger')
            return redirect(url_for('auth.register'))
        
        if len(username) < 3:
            flash('Имя пользователя должно содержать минимум 3 символа', 'danger')
            return redirect(url_for('auth.register'))
        
        if not is_valid_email(email):
            flash('Пожалуйста, введите корректный email', 'danger')
            return redirect(url_for('auth.register'))
        
        if len(password) < 6:
            flash('Пароль должен содержать минимум 6 символов', 'danger')
            return redirect(url_for('auth.register'))
        
        if password != password2:
            flash('Пароли не совпадают', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(username=username).first():
            flash('Это имя пользователя уже занято', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Этот email уже зарегистрирован', 'danger')
            return redirect(url_for('auth.register'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Поздравляем! Вы успешно зарегистрировались.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Регистрация')

@auth_blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно вышли из системы', 'success')
    return redirect(url_for('main.index'))
