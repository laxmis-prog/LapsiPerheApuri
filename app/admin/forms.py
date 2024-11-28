from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField, TextAreaField, DateField, TimeField
from wtforms.validators import DataRequired, Length

class AssignTaskForm(FlaskForm):
    user_id = SelectField('Käyttäjä', coerce=int, validators=[DataRequired()])
    task_id = SelectField('Tehtävä', coerce=int, validators=[DataRequired()])
    task_title = StringField('Otsikko', validators=[DataRequired(), Length(max=128)])
    task_description = TextAreaField('Kuvaus', validators=[DataRequired()])
    task_due_date = DateField('Eräpäivä', format='%Y-%m-%d', validators=[DataRequired()])
    task_time = TimeField('Aika', format='%H:%M', validators=[DataRequired()])
    task_category = SelectField('Kategoria', choices=[('Lääkäri', 'Lääkäri'), ('Koulu', 'Koulu'), ('Yksityinen', 'Yksityinen')], validators=[DataRequired()])
    task_status = SelectField('Tila', choices=[('Odottaa', 'Odottaa'), ('Suoritettu', 'Suoritettu')], validators=[DataRequired()])
    submit = SubmitField('Anna tehtävä')