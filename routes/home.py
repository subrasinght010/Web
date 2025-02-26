import logging
from flask import Blueprint, render_template, session
from models import Task
from utils import logger

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    try:
        tasks = []
        if 'user_id' in session:
            tasks = Task.query.filter_by(user_id=session['user_id']).all()
            logger.info(f"User {session['user_id']} accessed home with {len(tasks)} tasks.")
        else:
            logger.info("Anonymous user accessed home page.")

        return render_template('index.html', tasks=tasks)

    except Exception as e:
        logger.error(f"Error loading home page: {str(e)}", exc_info=True)
        return render_template('index.html', tasks=[])
