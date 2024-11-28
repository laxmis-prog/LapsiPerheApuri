from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import admin
from ..main import main
from .. import db
from ..models import Task, Feedback, User
from .forms import AssignTaskForm

@admin.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_administrator():
        flash('Sinulla ei ole oikeuksia nähdä tätä sivua.')
        return redirect(url_for('main.index'))

    # Fetch statistics
    total_users = User.query.count()
    total_tasks = Task.query.count()
    active_users = User.query.filter_by(confirmed=True).count()

    tasks = Task.query.all()
    feedbacks = Feedback.query.all()

    return render_template('admin/dashboard.html', tasks=tasks, feedbacks=feedbacks, 
                           total_users=total_users, total_tasks=total_tasks, active_users=active_users)



@admin.route('/assign_task', methods=['GET', 'POST'])
@login_required
def assign_task():
    if not current_user.is_administrator():
        flash('Sinulla ei ole oikeuksia nähdä tätä sivua.')
        return redirect(url_for('admin.admin_dashboard'))

    form = AssignTaskForm()

    # Ensure choices for user_id field are set properly
    form.user_id.choices = [(user.id, user.username) for user in User.query.all()]

    # Ensure choices for task_id field are set properly
    form.task_id.choices = [(task.task_id, task.title) for task in Task.query.all()]

    if form.validate_on_submit():
        # Fetch the selected task
        task = Task.query.get(form.task_id.data)
        if task:
            # Assign the task to the selected user
            task.user_id = form.user_id.data  # User receiving the task
            task.status = request.form.get('task_status')
            task.assigned_to = form.user_id.data  # Explicitly set assigned_to
            task.assigned_by = current_user.id  # Set the current admin's ID as assigned_by
            
            db.session.commit()
            flash('Tehtävä on annettu käyttäjälle.')
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash('Tehtävää ei löytynyt.')

    return render_template('admin/assign_task.html', form=form)

@admin.route('/admin/all_tasks')
@login_required
def all_tasks():
    tasks = Task.query.all()
    return render_template('admin/all_tasks.html', tasks=tasks)

@admin.route('/users')
@login_required
def users():
    if not current_user.is_administrator():
        flash('Sinulla ei ole oikeuksia nähdä tätä sivua.')
        return redirect(url_for('main.index'))

    # Fetch all users and active users
    all_users = User.query.all()
    active_users = User.query.filter_by(confirmed=True).all()

    return render_template('admin/users.html', all_users=all_users, active_users=active_users)



