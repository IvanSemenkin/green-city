from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from app.models import Event

class EventForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField('Описание', validators=[DataRequired()])
    date = DateTimeField('Дата и время', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    location = StringField('Место проведения', validators=[DataRequired(), Length(max=200)])
    event_type = SelectField('Тип мероприятия', validators=[DataRequired()], 
                           choices=[
                               ('subbotnik', 'Субботник'),
                               ('tree_planting', 'Посадка деревьев'),
                               ('eco_lecture', 'Эко-лекция'),
                               ('cleanup', 'Уборка территории'),
                               ('recycling', 'Сбор вторсырья'),
                               ('eco_festival', 'Эко-фестиваль'),
                               ('workshop', 'Мастер-класс'),
                               ('other', 'Другое')
                           ])
    submit = SubmitField('Сохранить')
