import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Task
from utils import logger


tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/tasks', methods=['GET', 'POST'])
@jwt_required()
def get_tasks():
    """Handles displaying and adding tasks"""
    try:
        current_identity = get_jwt_identity()
        user_id = current_identity.get("user_id")
        username= current_identity.get("username")

        if not user_id:
            logger.warning("JWT token is missing user_id")
            flash("Authentication failed.", "danger")
            return redirect(url_for('auth.login'))

        if request.method == 'POST':
            title = request.form.get('title')

            if not title:
                flash("Task title is required.", "danger")
                return redirect(url_for('tasks.get_tasks'))

            existing_task = Task.query.filter_by(title=title, user_id=user_id).first()
            if existing_task:
                flash("Task with this title already exists.", "warning")
                return redirect(url_for('tasks.get_tasks'))

            new_task = Task(title=title, user_id=user_id)
            db.session.add(new_task)

            try:
                db.session.commit()
                logger.info(f"Task '{title}' added by user {user_id}")
                flash("Task added successfully!", "success")
            except Exception as e:
                db.session.rollback()
                logger.error(f"Database error: {str(e)}", exc_info=True)
                flash("Database error occurred.", "danger")

            return redirect(url_for('tasks.get_tasks'))

        tasks = Task.query.filter_by(user_id=user_id).all()
        if not tasks:
            flash("No tasks found.", "info")

        return render_template('tasks.html', tasks=tasks,username=username)

    except Exception as e:
        logger.error(f"Error in get_tasks: {str(e)}", exc_info=True)
        flash("An error occurred while loading tasks.", "danger")
        return redirect(url_for('home.home'))



@tasks_bp.route('/tasks/edit/<int:task_id>', methods=['POST'])
@jwt_required()
def edit_task(task_id):
    """Handles editing a task"""
    try:
        current_identity = get_jwt_identity()
        user_id = current_identity.get("user_id")
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            logger.warning(f"Edit failed: Task ID {task_id} not found for user {user_id}")
            flash("Task not found.", "danger")
            return redirect(url_for('tasks.get_tasks'))

        title = request.form.get('title')
        if not title:
            flash("Task title is required.", "danger")
            return redirect(url_for('tasks.get_tasks'))

        task.title = title
        task.completed = request.form.get('completed') == "True"
        db.session.commit()

        logger.info(f"Task ID {task_id} updated by user {user_id}")
        flash("Task updated successfully!", "success")
        return redirect(url_for('tasks.get_tasks'))

    except Exception as e:
        logger.error(f"Error in edit_task: {str(e)}", exc_info=True)
        flash("An error occurred while updating the task.", "danger")
        return redirect(url_for('tasks.get_tasks'))

@tasks_bp.route('/tasks/toggle/<int:task_id>', methods=['GET'])
@jwt_required()
def toggle_task(task_id):
    """Handles toggling a task's completion status"""
    try:
        current_identity = get_jwt_identity()
        user_id = current_identity.get("user_id")

        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            logger.warning(f"Toggle failed: Task ID {task_id} not found for user {user_id}")
            flash("Task not found.", "danger")
            return redirect(url_for('tasks.get_tasks'))

        task.completed = not task.completed
        db.session.commit()

        logger.info(f"Task ID {task_id} toggled by user {user_id} - New status: {'Completed' if task.completed else 'Pending'}")
        flash("Task status updated!", "success")
        return redirect(url_for('tasks.get_tasks'))

    except Exception as e:
        logger.error(f"Error in toggle_task: {str(e)}", exc_info=True)
        flash("An error occurred while toggling the task.", "danger")
        return redirect(url_for('tasks.get_tasks'))

@tasks_bp.route('/tasks/delete/<int:task_id>', methods=['POST','GET'])
@jwt_required()
def delete_task(task_id):
    """Handles deleting a task"""
    try:
        current_identity = get_jwt_identity()
        user_id = current_identity.get("user_id")

        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            logger.warning(f"Delete failed: Task ID {task_id} not found for user {user_id}")
            flash("Task not found.", "danger")
            return redirect(url_for('tasks.get_tasks'))

        db.session.delete(task)
        db.session.commit()

        logger.info(f"Task ID {task_id} deleted by user {user_id}")
        flash("Task deleted successfully!", "success")
        return redirect(url_for('tasks.get_tasks'))

    except Exception as e:
        logger.error(f"Error in delete_task: {str(e)}", exc_info=True)
        flash("An error occurred while deleting the task.", "danger")
        return redirect(url_for('tasks.get_tasks'))
