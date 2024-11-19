
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField
from wtforms.validators import DataRequired, Length

class AssignTaskForm(FlaskForm):
    user_id = SelectField('Käyttäjä', coerce=int, validators=[DataRequired()])
    task_id = SelectField('Tehtävä', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Anna tehtävä')

class EditCategoryForm(FlaskForm):
    category = StringField('Kategoria', validators=[DataRequired(), Length(max=64)])
    submit = SubmitField('Muokkaa kategoriaa')