from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField, TextAreaField, DateField, TimeField
from wtforms.validators import DataRequired, Length

class AssignTaskForm(FlaskForm):
    # User selection field, assuming the user IDs are integers.
    user_id = SelectField('Käyttäjä', coerce=int, validators=[DataRequired()])

     
    # Task ID field - Added here
    task_id = SelectField('Tehtävä', coerce=int, validators=[DataRequired()])
    
    # Task title field.
    task_title = StringField('Otsikko', validators=[DataRequired(), Length(max=128)])
    
    # Task description field.
    task_description = TextAreaField('Kuvaus', validators=[DataRequired()])
    
    # Due date field.
    task_due_date = DateField('Eräpäivä', format='%Y-%m-%d', validators=[DataRequired()])
    
    # Task time field.
    task_time = TimeField('Aika', format='%H:%M', validators=[DataRequired()])
    
    # Task category field with predefined options.
    task_category = SelectField('Kategoria', choices=[('Lääkäri', 'Lääkäri'), ('Koulu', 'Koulu'), ('Yksityinen', 'Yksityinen')], validators=[DataRequired()])
    
    # Task status field with predefined options.
    task_status = SelectField('Tila', choices=[('Odottaa', 'Odottaa'), ('Suoritettu', 'Suoritettu')], validators=[DataRequired()])
    
    # Submit button
    submit = SubmitField('Anna tehtävä')