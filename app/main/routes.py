from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Event, EcoChallenge, EcoTip, Tree, User, GreenZone
from datetime import datetime
from flask_login import login_required, current_user
from app import db

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
@main_blueprint.route('/index')
def index():
    return render_template('index.html')

@main_blueprint.route('/events')
def events():
    selected_type = request.args.get('type', 'all')
    
    # Получаем все мероприятия
    query = Event.query.order_by(Event.date.asc())
    
    # Фильтруем по типу, если выбран конкретный тип
    if selected_type != 'all':
        query = query.filter(Event.event_type == selected_type)
    
    # Получаем будущие мероприятия
    future_events = query.filter(Event.date >= datetime.now()).all()
    
    # Получаем прошедшие мероприятия
    past_events = Event.query.filter(Event.date < datetime.now()).order_by(Event.date.desc()).all()
    
    return render_template('events.html',
                         future_events=future_events,
                         past_events=past_events,
                         event_types=Event.EVENT_TYPES,
                         selected_type=selected_type)

@main_blueprint.route('/map')
def map():
    try:
        green_zones = GreenZone.query.all()
        green_zones_json = [zone.to_dict() for zone in green_zones]
        return render_template('map.html', green_zones=green_zones_json)
    except Exception as e:
        print(f"Ошибка при загрузке зеленых зон: {e}")
        return render_template('map.html', green_zones=[])

@main_blueprint.route('/tips')
def tips():
    # Получаем параметры фильтрации из запроса
    selected_category = request.args.get('category', 'all')
    selected_difficulty = request.args.get('difficulty', 'all')
    
    # Начинаем с базового запроса
    query = EcoTip.query
    
    # Фильтруем по категории, если выбрана
    if selected_category != 'all':
        query = query.filter(EcoTip.category == selected_category)
    
    # Фильтруем по сложности, если выбрана
    if selected_difficulty != 'all':
        query = query.filter(EcoTip.difficulty == selected_difficulty)
    
    # Получаем отфильтрованные советы
    tips = query.all()
    
    return render_template('tips.html', 
                           tips=tips, 
                           categories=EcoTip.CATEGORIES, 
                           difficulty_levels=EcoTip.DIFFICULTY_LEVELS,
                           selected_category=selected_category,
                           selected_difficulty=selected_difficulty)

@main_blueprint.route('/trees', methods=['GET', 'POST'])
def trees():
    if request.method == 'POST' and current_user.is_authenticated:
        # Обработка добавления нового дерева
        species = request.form.get('species')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        description = request.form.get('description', '')
        status = request.form.get('status', 'healthy')
        
        # Валидация данных
        if not all([species, latitude, longitude]):
            flash('Пожалуйста, заполните все обязательные поля', 'danger')
            return redirect(url_for('main.trees'))
        
        try:
            new_tree = Tree(
                species=species,
                latitude=float(latitude),
                longitude=float(longitude),
                description=description,
                status=status,
                planted_by=current_user.id
            )
            db.session.add(new_tree)
            db.session.commit()
            flash('Дерево успешно добавлено!', 'success')
            return redirect(url_for('main.trees'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при добавлении дерева: {str(e)}', 'danger')
    
    # Получаем параметры фильтрации
    selected_species = request.args.get('species', 'all')
    selected_status = request.args.get('status', 'all')
    
    # Начинаем с базового запроса
    query = Tree.query
    
    # Фильтруем по виду дерева
    if selected_species != 'all':
        query = query.filter(Tree.species == selected_species)
    
    # Фильтруем по статусу
    if selected_status != 'all':
        query = query.filter(Tree.status == selected_status)
    
    # Получаем отфильтрованные деревья
    trees = query.order_by(Tree.planting_date.desc()).all()
    
    # Статистика
    total_trees = Tree.query.count()
    trees_by_species = db.session.query(
        Tree.species, 
        db.func.count(Tree.id)
    ).group_by(Tree.species).all()
    
    return render_template('trees.html', 
                           trees=trees, 
                           total_trees=total_trees,
                           trees_by_species=trees_by_species,
                           tree_species=Tree.TREE_SPECIES, 
                           tree_statuses=Tree.TREE_STATUSES,
                           selected_species=selected_species,
                           selected_status=selected_status)

@main_blueprint.route('/challenges')
def challenges():
    now = datetime.now()
    
    # Получаем активные челленджи (текущая дата между начальной и конечной датой)
    active_challenges = EcoChallenge.query.filter(
        EcoChallenge.start_date <= now,
        EcoChallenge.end_date >= now
    ).all()
    
    # Получаем предстоящие челленджи (начальная дата в будущем)
    upcoming_challenges = EcoChallenge.query.filter(
        EcoChallenge.start_date > now
    ).order_by(EcoChallenge.start_date.asc()).all()
    
    # Получаем завершенные челленджи (конечная дата в прошлом)
    completed_challenges = EcoChallenge.query.filter(
        EcoChallenge.end_date < now
    ).order_by(EcoChallenge.end_date.desc()).all()
    
    return render_template('challenges.html',
                         active_challenges=active_challenges,
                         upcoming_challenges=upcoming_challenges,
                         completed_challenges=completed_challenges)

@main_blueprint.route('/challenges/<int:id>/join', methods=['POST'])
@login_required
def join_challenge(id):
    challenge = EcoChallenge.query.get_or_404(id)
    
    # Проверяем, что челлендж активен
    now = datetime.now()
    if not (challenge.start_date <= now <= challenge.end_date):
        flash('Этот эко-челлендж сейчас недоступен для участия', 'danger')
        return redirect(url_for('main.challenges'))
    
    # Проверяем, не участвует ли уже пользователь
    if challenge in current_user.challenges:
        flash('Вы уже участвуете в этом эко-челлендже', 'info')
        return redirect(url_for('main.challenges'))
    
    # Добавляем пользователя к челленджу
    current_user.challenges.append(challenge)
    db.session.commit()
    
    flash('Вы успешно присоединились к эко-челленджу!', 'success')
    return redirect(url_for('main.challenges'))

@main_blueprint.route('/become_admin', methods=['GET', 'POST'])
@login_required
def become_admin():
    if request.method == 'POST':
        password = request.form.get('password')
        
        # Проверка пароля
        if password == 'parols01':
            return render_template('admin/assign_admin.html', users=User.query.all())
        else:
            flash('Неверный пароль', 'danger')
            return redirect(url_for('main.become_admin'))
    
    return render_template('admin/password_check.html')

@main_blueprint.route('/assign_admin', methods=['POST'])
@login_required
def assign_admin():
    # Проверка пароля повторно
    password = request.form.get('password')
    user_id = request.form.get('user_id')
    
    if password != 'parols01':
        flash('Неверный пароль', 'danger')
        return redirect(url_for('main.become_admin'))
    
    user = User.query.get_or_404(user_id)
    
    # Назначаем администратора
    user.is_admin = True
    
    try:
        db.session.commit()
        flash(f'Пользователь {user.username} назначен администратором', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при назначении администратора: {str(e)}', 'danger')
    
    return redirect(url_for('main.index'))
