import logging
from config import Config
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, Task
from utils import logger


tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['GET', 'POST'])
def get_tasks():
    """Handles displaying and adding tasks"""
    try:
        if 'user_id' not in session:
            flash("Please log in to access tasks.", "warning")
            return redirect(url_for('auth.login'))

        if request.method == 'POST':
            title = request.form['title']
            new_task = Task(title=title, user_id=session['user_id'])
            db.session.add(new_task)
            db.session.commit()
            logger.info(f"Task '{title}' added by user {session['user_id']}")
            flash("Task added successfully!", "success")
            return redirect(url_for('tasks.get_tasks'))

        tasks = Task.query.filter_by(user_id=session['user_id']).all()
        return render_template('tasks.html', tasks=tasks)

    except Exception as e:
        logger.error(f"Error in get_tasks: {str(e)}", exc_info=True)
        flash("An error occurred while loading tasks.", "danger")
        return redirect(url_for('home.home'))


@tasks_bp.route('/tasks/edit/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    """Handles editing a task"""
    try:
        if 'user_id' not in session:
            flash("Please log in to edit tasks.", "warning")
            return redirect(url_for('auth.login'))

        task = Task.query.filter_by(id=task_id, user_id=session['user_id']).first()
        if not task:
            logger.warning(f"Edit failed: Task ID {task_id} not found for user {session['user_id']}")
            flash("Task not found.", "danger")
            return redirect(url_for('tasks.get_tasks'))

        task.title = request.form['title']
        task.completed = request.form['completed'] == "True"
        db.session.commit()

        logger.info(f"Task ID {task_id} updated by user {session['user_id']}")
        flash("Task updated successfully!", "success")
        return redirect(url_for('tasks.get_tasks'))

    except Exception as e:
        logger.error(f"Error in edit_task: {str(e)}", exc_info=True)
        flash("An error occurred while updating the task.", "danger")
        return redirect(url_for('tasks.get_tasks'))


@tasks_bp.route('/tasks/toggle/<int:task_id>', methods=['GET'])
def toggle_task(task_id):
    """Handles toggling a task's completion status"""
    try:
        if 'user_id' not in session:
            flash("Please log in to toggle tasks.", "warning")
            return redirect(url_for('auth.login'))

        task = Task.query.filter_by(id=task_id, user_id=session['user_id']).first()
        if not task:
            logger.warning(f"Toggle failed: Task ID {task_id} not found for user {session['user_id']}")
            flash("Task not found.", "danger")
            return redirect(url_for('tasks.get_tasks'))

        task.completed = not task.completed
        db.session.commit()

        logger.info(f"Task ID {task_id} toggled by user {session['user_id']} - New status: {'Completed' if task.completed else 'Pending'}")
        flash("Task status updated!", "success")
        return redirect(url_for('tasks.get_tasks'))

    except Exception as e:
        logger.error(f"Error in toggle_task: {str(e)}", exc_info=True)
        flash("An error occurred while toggling the task.", "danger")
        return redirect(url_for('tasks.get_tasks'))


@tasks_bp.route('/tasks/delete/<int:task_id>')
def delete_task(task_id):
    """Handles deleting a task"""
    try:
        if 'user_id' not in session:
            flash("Please log in to delete tasks.", "warning")
            return redirect(url_for('auth.login'))

        task = Task.query.filter_by(id=task_id, user_id=session['user_id']).first()
        if not task:
            logger.warning(f"Delete failed: Task ID {task_id} not found for user {session['user_id']}")
            flash("Task not found.", "danger")
            return redirect(url_for('tasks.get_tasks'))

        db.session.delete(task)
        db.session.commit()

        logger.info(f"Task ID {task_id} deleted by user {session['user_id']}")
        flash("Task deleted successfully!", "success")
        return redirect(url_for('tasks.get_tasks'))

    except Exception as e:
        logger.error(f"Error in delete_task: {str(e)}", exc_info=True)
        flash("An error occurred while deleting the task.", "danger")
        return redirect(url_for('tasks.get_tasks'))
