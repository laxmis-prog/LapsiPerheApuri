from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, BooleanField, SelectField,\
    SubmitField, FileField, DateField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, User
from flask_wtf.file import FileAllowed, FileRequired

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class TaskForm(FlaskForm):
    member_name = StringField('Jäsenen nimi', validators=[Length(max=64)])
    title = StringField('Otsikko', validators=[DataRequired(), Length(max=128)])
    description = TextAreaField('Kuvaus')
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()])
    category = StringField('Kategoria', validators=[Length(max=64)])
    status = SelectField('Tila', choices=[('pending', 'Pending'), ('completed', 'Completed')])
    submit = SubmitField('Lähetä')

class FeedbackForm(FlaskForm):
    name = StringField('Nimi', validators=[DataRequired(), Length(max=64)])
    email = StringField('Sähköposti', validators=[DataRequired(), Length(max=64)])
    message = TextAreaField('Viesti', validators=[DataRequired()])
    submit = SubmitField('Lähetä')


class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    profile_picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Submit')
    
class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    profile_picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
