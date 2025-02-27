import logging
from flask import render_template, redirect, url_for, flash, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from werkzeug.exceptions import Unauthorized
from models import Task
from utils import logger

home_bp = Blueprint('home', __name__)

import logging

logger = logging.getLogger(__name__)

@home_bp.route('/')
def home():
    try:
        try:
            verify_jwt_in_request()
            current_identity = get_jwt_identity()
        except Unauthorized:
            flash("You must be logged in to access this page.", "warning")
            return redirect(url_for("auth.login"))  # Redirect to your login route

        tasks = []
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
        flash("An error occurred while loading the page.", "danger")
        return redirect(url_for("auth.login"))

