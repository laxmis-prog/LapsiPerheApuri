import os
from flask import render_template, redirect, url_for, flash, current_app, request
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from . import main
from .. import db
from ..models import User
from .forms import EditProfileForm

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data

        # Check if a profile picture was uploaded
        if form.profile_picture.data:
            filename = secure_filename(form.profile_picture.data.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            form.profile_picture.data.save(file_path)
            
            # Update user's profile picture field
            current_user.profile_picture = filename

        # Save all changes to the database
        db.session.add(current_user)
        db.session.commit()
        
        flash('Your profile has been updated.')
        return redirect(url_for('main.user', username=current_user.username))
    
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)