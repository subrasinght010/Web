import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_jwt_extended import create_access_token 

from models import db, User
from utils import logger
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration"""
    try:
        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            username = request.form['username']
            password = request.form['password']

            if User.query.filter_by(username=username).first():
                logger.warning(f"Registration failed: User '{username}' already exists.")
                flash("User already exists. Try a different username.", "danger")
                return redirect(url_for('auth.register'))

            new_user = User(
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=User.hash_password(password)
            )

            db.session.add(new_user)
            db.session.commit()
            logger.info(f"New user registered: {username}")

            flash("Registration successful. You can now log in.", "success")
            return redirect(url_for('auth.login'))

        return render_template('register.html')

    except Exception as e:
        logger.error(f"Error during registration: {str(e)}", exc_info=True)
        flash("An error occurred. Please try again.", "danger")
        return redirect(url_for('auth.register'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login"""
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()

            if not user or not user.check_password(password):
                logger.warning(f"Failed login attempt for user: {username}")
                flash("Invalid credentials. Please try again.", "danger")
                return redirect(url_for('auth.login'))

            access_token = create_access_token(identity={"user_id": str(user.id), "username": str(username)})

            response = make_response(redirect(url_for('home.home')))
            response.set_cookie('jwt_token', access_token, httponly=True, secure=False)

            logger.info(f"User '{username}' logged in successfully")
            flash("Login successful!", "success")
            return response

        return render_template('login.html')

    except Exception as e:
        logger.error(f"Error during login: {str(e)}", exc_info=True)
        flash("An error occurred. Please try again.", "danger")
        return redirect(url_for('auth.login'))



@auth_bp.route('/logout')
def logout():
    """Handles user logout"""
    try:
        response = make_response(redirect(url_for('auth.login')))
        response.set_cookie('jwt_token', '', expires=0) 

        logger.info(f"User logged out successfully")
        flash("You have been logged out.", "info")
        return response

    except Exception as e:
        logger.error(f"Error during logout: {str(e)}", exc_info=True)
        flash("An error occurred while logging out.", "danger")
        return redirect(url_for('auth.login'))
