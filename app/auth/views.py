from flask import render_template, redirect, request, url_for, flash
from datetime import datetime
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User
from ..email import send_email
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            if user.is_administrator():
                return redirect(url_for('admin.admin_dashboard'))
            return redirect(url_for('main.tasks'))  # Redirect to tasks page after login
        flash('Virheellinen käyttäjänimi tai salasana.')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # User passed all form validations
        user = User(email=form.email.data.lower(),
                    username=form.username.data,
                    password=form.password.data,
                    member_since=datetime.utcnow())
        
        # Add user to the database
        db.session.add(user)
        db.session.commit()
        
        # Send confirmation email
        token = user.generate_confirmation_token()
        send_email(user.email, 'Vahvista tilisi',
                   'auth/email/confirm', user=user, token=token)
        
        flash('Vahvistusviesti on lähetetty sähköpostiosoitteeseesi.', 'success')
        return redirect(url_for('auth.login'))
    else:
        # Debugging: Output validation errors to the console
        print("Form validation errors:", form.errors)

    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('Tilisi on vahvistettu. Kiitos!')
    else:
        flash('Vahvistuslinkki on virheellinen tai vanhentunut.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Vahvista tilisi',
               'auth/email/confirm', user=current_user, token=token)
    flash('Uusi vahvistusviesti on lähetetty sähköpostiosoitteeseesi.')
    return redirect(url_for('main.index'))

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Salasanasi on päivitetty.')
            return redirect(url_for('main.index'))
        else:
            flash('Virheellinen salasana.')
    return render_template("auth/change_password.html", form=form)

@auth.route('/reset_password_request', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Nollaa salasanasi',
                       'auth/email/reset_password', user=user, token=token)
        flash('Sinulle on lähetetty sähköposti,jossa on ohjeet salasanan nollaamiseksi')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Salasanasi on päivitetty.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change_email_request', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        new_email = form.email.data.lower()
        token = current_user.generate_email_change_token(new_email)
        send_email(new_email, 'Vaihda sähköpostiosoite',
                   'auth/email/change_email', user=current_user, token=token)
        flash('Sähköpostiosoitteen vaihtolinkki on lähetetty sähköpostiisi.')
        return redirect(url_for('main.index'))
    return render_template('auth/change_email_request.html', form=form)

@auth.route('/change_email/<token>', methods=['GET', 'POST'])
@login_required
def change_email(token):
    if not current_user.confirm(token):
        flash('Virheellinen tai vanhentunut vahvistuslinkki.')
        return redirect(url_for('main.index'))
    form = ChangeEmailForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        db.session.add(current_user)
        db.session.commit()
        flash('Sähköpostiosoitteesi on päivitetty.')
        return redirect(url_for('main.index'))
    return render_template('auth/change_email.html', form=form)

