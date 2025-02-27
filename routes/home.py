import logging
from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Task, User
from utils import logger

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@jwt_required()
def home():
    try:
        tasks = []
        current_identity = get_jwt_identity()
        current_user_id = current_identity.get("user_id")
        username = current_identity.get("username")
        if current_user_id:
            tasks = Task.query.filter_by(user_id=current_user_id).all()
            logger.info(f"User {current_user_id} accessed home with {len(tasks)} tasks.")
        else:
            logger.info("Anonymous user accessed home page.")

        return render_template('index.html', tasks=tasks, username=username)

    except Exception as e:
        logger.error(f"Error loading home page: {str(e)}", exc_info=True)
        return render_template('index.html', tasks=[], username='NA')


@home_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    """A protected route that requires a valid JWT."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user:
        return f'Hello, {user.username}!'
    else:
        return 'User not found', 404
