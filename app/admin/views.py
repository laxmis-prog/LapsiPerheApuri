from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from . import admin
from .. import db
from ..models import Task, Feedback, User
from .forms import AssignTaskForm, EditCategoryForm

@admin.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Sinulla ei ole oikeuksia nähdä tätä sivua.')
        return redirect(url_for('main.index'))
    tasks = Task.query.all()
    feedbacks = Feedback.query.all()
    return render_template('admin/dashboard.html', tasks=tasks, feedbacks=feedbacks)

@admin.route('/assign_task', methods=['GET', 'POST'])
@login_required
def assign_task():
    if not current_user.is_admin:
        flash('Sinulla ei ole oikeuksia nähdä tätä sivua.')
        return redirect(url_for('main.index'))
    form = AssignTaskForm()
    form.user_id.choices = [(user.id, user.username) for user in User.query.all()]
    form.task_id.choices = [(task.id, task.title) for task in Task.query.all()]
    if form.validate_on_submit():
        task = Task.query.get(form.task_id.data)
        task.user_id = form.user_id.data
        db.session.commit()
        flash('Tehtävä on annettu käyttäjälle.')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/assign_task.html', form=form)

@admin.route('/edit_category/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_category(task_id):
    if not current_user.is_admin:
        flash('Sinulla ei ole oikeuksia nähdä tätä sivua.')
        return redirect(url_for('main.index'))
    task = Task.query.get_or_404(task_id)
    form = EditCategoryForm()
    if form.validate_on_submit():
        task.category = form.category.data
        db.session.commit()
        flash('Kategoria on päivitetty.')
        return redirect(url_for('admin.admin_dashboard'))
    form.category.data = task.category
    return render_template('admin/edit_category.html', form=form, task=task)