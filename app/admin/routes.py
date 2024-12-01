from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Event, EcoChallenge, User, EcoTip, Tree, db
from app.admin.forms import EventForm
from datetime import datetime
from functools import wraps

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Доступ запрещен. Требуются права администратора.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_blueprint.route('/dashboard')
@admin_required
def dashboard():
    events_count = Event.query.count()
    challenges_count = EcoChallenge.query.count()
    users_count = User.query.count()
    return render_template('admin/dashboard.html', 
                         events_count=events_count,
                         challenges_count=challenges_count,
                         users_count=users_count)

# События
@admin_blueprint.route('/events')
@admin_required
def events():
    events = Event.query.order_by(Event.date.desc()).all()
    return render_template('admin/events.html', events=events, event_types=Event.EVENT_TYPES)

@admin_blueprint.route('/events/add', methods=['GET', 'POST'])
@admin_required
def add_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            date=form.date.data,
            location=form.location.data,
            event_type=form.event_type.data,
            organizer_id=current_user.id
        )
        db.session.add(event)
        db.session.commit()
        flash('Мероприятие успешно добавлено!', 'success')
        return redirect(url_for('admin.events'))
    return render_template('admin/event_form.html', form=form)

@admin_blueprint.route('/events/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_event(id):
    event = Event.query.get_or_404(id)
    form = EventForm(obj=event)
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.date = form.date.data
        event.location = form.location.data
        event.event_type = form.event_type.data
        db.session.commit()
        flash('Мероприятие успешно обновлено!', 'success')
        return redirect(url_for('admin.events'))
    return render_template('admin/event_form.html', form=form, event=event)

@admin_blueprint.route('/events/<int:id>/delete', methods=['POST'])
@admin_required
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    flash('Мероприятие успешно удалено!', 'success')
    return redirect(url_for('admin.events'))

# Эко-челленджи
@admin_blueprint.route('/challenges')
@admin_required
def challenges():
    challenges = EcoChallenge.query.order_by(EcoChallenge.start_date.desc()).all()
    return render_template('admin/challenges.html', challenges=challenges)

@admin_blueprint.route('/challenges/add', methods=['GET', 'POST'])
@admin_required
def add_challenge():
    if request.method == 'POST':
        challenge = EcoChallenge(
            title=request.form['title'],
            description=request.form['description'],
            start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d'),
            end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%d'),
            points=int(request.form['points'])
        )
        db.session.add(challenge)
        db.session.commit()
        flash('Эко-челлендж успешно добавлен!', 'success')
        return redirect(url_for('admin.challenges'))
    return render_template('admin/challenge_form.html')

@admin_blueprint.route('/challenges/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_challenge(id):
    challenge = EcoChallenge.query.get_or_404(id)
    if request.method == 'POST':
        challenge.title = request.form['title']
        challenge.description = request.form['description']
        challenge.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        challenge.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
        challenge.points = int(request.form['points'])
        db.session.commit()
        flash('Эко-челлендж успешно обновлен!', 'success')
        return redirect(url_for('admin.challenges'))
    return render_template('admin/challenge_form.html', challenge=challenge)

@admin_blueprint.route('/challenges/<int:id>/delete', methods=['POST'])
@admin_required
def delete_challenge(id):
    challenge = EcoChallenge.query.get_or_404(id)
    db.session.delete(challenge)
    db.session.commit()
    flash('Эко-челлендж успешно удален!', 'success')
    return redirect(url_for('admin.challenges'))

# Пользователи
@admin_blueprint.route('/users')
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_blueprint.route('/users/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # Предотвращаем удаление собственного аккаунта
    if user.id == current_user.id:
        flash('Вы не можете удалить свой собственный аккаунт', 'danger')
        return redirect(url_for('admin.manage_users'))
    
    # Удаляем связанные записи
    Tree.query.filter_by(planted_by=user.id).delete()
    Event.query.filter_by(organizer_id=user.id).delete()
    
    db.session.delete(user)
    db.session.commit()
    
    flash(f'Пользователь {user.username} успешно удален', 'success')
    return redirect(url_for('admin.manage_users'))

@admin_blueprint.route('/users/toggle_admin/<int:user_id>', methods=['POST'])
@admin_required
def toggle_admin(user_id):
    user = User.query.get_or_404(user_id)
    
    # Предотвращаем изменение роли собственного аккаунта
    if user.id == current_user.id:
        flash('Вы не можете изменить свою собственную роль', 'danger')
        return redirect(url_for('admin.manage_users'))
    
    # Переключаем роль администратора
    user.is_admin = not user.is_admin
    
    try:
        db.session.commit()
        status = "назначен администратором" if user.is_admin else "лишен прав администратора"
        flash(f'Пользователь {user.username} {status}', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при изменении роли: {str(e)}', 'danger')
    
    return redirect(url_for('admin.manage_users'))

# Советы
@admin_blueprint.route('/tips')
@admin_required
def manage_tips():
    tips = EcoTip.query.all()
    return render_template('admin/tips.html', 
                           tips=tips, 
                           categories=EcoTip.CATEGORIES, 
                           difficulty_levels=EcoTip.DIFFICULTY_LEVELS)

@admin_blueprint.route('/tips/add', methods=['GET', 'POST'])
@admin_required
def add_tip():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        difficulty = request.form.get('difficulty')
        points = request.form.get('points', 0)
        
        if not all([title, description, category, difficulty]):
            flash('Пожалуйста, заполните все обязательные поля', 'danger')
            return redirect(url_for('admin.add_tip'))
        
        try:
            new_tip = EcoTip(
                title=title,
                description=description,
                category=category,
                difficulty=difficulty,
                points=int(points)
            )
            db.session.add(new_tip)
            db.session.commit()
            
            flash('Совет успешно добавлен', 'success')
            return redirect(url_for('admin.manage_tips'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при добавлении совета: {str(e)}', 'danger')
    
    return render_template('admin/tip_form.html', 
                           categories=EcoTip.CATEGORIES, 
                           difficulty_levels=EcoTip.DIFFICULTY_LEVELS)

@admin_blueprint.route('/tips/edit/<int:tip_id>', methods=['GET', 'POST'])
@admin_required
def edit_tip(tip_id):
    tip = EcoTip.query.get_or_404(tip_id)
    
    if request.method == 'POST':
        tip.title = request.form.get('title')
        tip.description = request.form.get('description')
        tip.category = request.form.get('category')
        tip.difficulty = request.form.get('difficulty')
        tip.points = int(request.form.get('points', 0))
        
        try:
            db.session.commit()
            flash('Совет успешно обновлен', 'success')
            return redirect(url_for('admin.manage_tips'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при обновлении совета: {str(e)}', 'danger')
    
    return render_template('admin/tip_form.html', 
                           tip=tip, 
                           categories=EcoTip.CATEGORIES, 
                           difficulty_levels=EcoTip.DIFFICULTY_LEVELS)

@admin_blueprint.route('/tips/delete/<int:tip_id>', methods=['POST'])
@admin_required
def delete_tip(tip_id):
    tip = EcoTip.query.get_or_404(tip_id)
    
    try:
        db.session.delete(tip)
        db.session.commit()
        
        flash('Совет успешно удален', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при удалении совета: {str(e)}', 'danger')
    
    return redirect(url_for('admin.manage_tips'))
