import os
from flask import render_template, redirect, url_for, flash, current_app, request
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from . import main
from .forms import TaskForm
from .. import db
from ..models import User
from ..models import Task
from .forms import EditProfileForm

@main.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    print("Before checking authentication")  # Add a simple print statement before
    print("User is authenticated:", current_user.is_authenticated)  # This will print in the console.
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            category=form.category.data,
            status=form.status.data,
            user_id=current_user.id,
            member_name=current_user.username 
        )
        db.session.add(task)
        db.session.commit()
        flash('Task created successfully.')
        return redirect(url_for('main.tasks'))
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.due_date).all()
    return render_template('tasks.html', form=form, tasks=tasks)

@main.route('/tasks/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.due_date = form.due_date.data
        task.category = form.category.data
        task.status = form.status.data
        task.member_name = form.member_name.data
        db.session.commit()
        flash('Task updated successfully.')
        return redirect(url_for('main.tasks'))
    return render_template('edit_task.html', form=form, task=task)


@main.route('/tasks/delete/<int:id>', methods=['POST'])
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully.')
    return redirect(url_for('main.tasks'))

@main.route('/tasks/status/<int:id>', methods=['POST'])
@login_required
def update_task_status(id):
    task = Task.query.get_or_404(id)
    task.status = request.form['status']
    db.session.commit()
    flash('Task status updated successfully.')
    return redirect(url_for('main.tasks'))

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

