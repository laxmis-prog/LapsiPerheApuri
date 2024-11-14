from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    email = StringField('Sähköposti', validators=[
        DataRequired(message='Täytä tämä kenttä'),
        Email(message='Anna kelvollinen sähköpostiosoite')
    ])
    password = PasswordField('Salasana', validators=[
        DataRequired(message='Täytä tämä kenttä')
    ])
    remember_me = BooleanField('Muista minut')
    submit = SubmitField('Kirjaudu sisään')

class RegistrationForm(FlaskForm):
    email = StringField('Sähköposti', validators=[
        DataRequired(message='Täytä tämä kenttä'),
        Email(message='Anna kelvollinen sähköpostiosoite')
    ])
    username = StringField('Käyttäjänimi', validators=[
        DataRequired(message='Täytä tämä kenttä'),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Käyttäjänimessä saa olla vain kirjaimia, numeroita, pisteitä tai alaviivoja.')
    ])
    password = PasswordField('Salasana', validators=[
        DataRequired(message='Täytä tämä kenttä'),
        EqualTo('password2', message='Salasanojen on oltava samat.')
    ])
    password2 = PasswordField('Vahvista salasana', validators=[
        DataRequired(message='Täytä tämä kenttä')
    ])
    submit = SubmitField('Rekisteröidy')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Sähköposti on jo rekisteröity.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Käyttäjänimi on jo käytössä.')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Vanha salasana', validators=[
        DataRequired(message='Täytä tämä kenttä')
    ])
    password = PasswordField('Uusi salasana', validators=[
        DataRequired(message='Täytä tämä kenttä'),
        EqualTo('password2', message='Salasanojen on oltava samat.')
    ])
    password2 = PasswordField('Vahvista uusi salasana', validators=[
        DataRequired(message='Täytä tämä kenttä')
    ])
    submit = SubmitField('Päivitä salasana')

class PasswordResetRequestForm(FlaskForm):
    email = StringField('Sähköposti', validators=[
        DataRequired(message='Täytä tämä kenttä'),
        Email(message='Anna kelvollinen sähköpostiosoite')
    ])
    submit = SubmitField('Nollaa salasana')

class PasswordResetForm(FlaskForm):
    password = PasswordField('Uusi salasana', validators=[
        DataRequired(message='Täytä tämä kenttä'),
        EqualTo('password2', message='Salasanojen on oltava samat.')
    ])
    password2 = PasswordField('Vahvista salasana', validators=[
        DataRequired(message='Täytä tämä kenttä')
    ])
    submit = SubmitField('Nollaa salasana')

class ChangeEmailForm(FlaskForm):
    email = StringField('Uusi sähköposti', validators=[
        DataRequired(message='Täytä tämä kenttä'),
        Length(1, 64, message='Sähköpostin on oltava 1-64 merkkiä pitkä'),
        Email(message='Anna kelvollinen sähköpostiosoite')
    ])
    password = PasswordField('Salasana', validators=[
        DataRequired(message='Täytä tämä kenttä')
    ])
    submit = SubmitField('Päivitä sähköpostiosoite')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Sähköposti on jo rekisteröity.')
