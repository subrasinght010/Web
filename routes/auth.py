import logging
from config import Config
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
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

            session['user_id'] = new_user.id
            session['username'] = f"{new_user.first_name} {new_user.last_name}"
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
        # import ipdb;ipdb.set_trace()
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()

            if not user or not user.check_password(password):
                logger.warning(f"Failed login attempt for user: {username}")
                flash("Invalid credentials. Please try again.", "danger")
                return redirect(url_for('auth.login'))

            session['user_id'] = user.id
            session['username'] = f"{user.first_name} {user.last_name}"
            logger.info(f"User '{username}' logged in successfully")
            print(f"User '{username}' logged in successfully")

            flash("Login successful!", "success")
            return redirect(url_for('home.home'))

        return render_template('login.html')

    except Exception as e:
        logger.error(f"Error during login: {str(e)}", exc_info=True)
        flash("An error occurred. Please try again.", "danger")
        return redirect(url_for('auth.login'))


@auth_bp.route('/logout')
def logout():
    """Handles user logout"""
    try:
        username = session.get('username', 'Unknown')
        session.pop('user_id', None)
        session.pop('username', None)
        logger.info(f"User '{username}' logged out successfully")

        flash("You have been logged out.", "info")
        return redirect(url_for('auth.login'))

    except Exception as e:
        logger.error(f"Error during logout: {str(e)}", exc_info=True)
        flash("An error occurred while logging out.", "danger")
        return redirect(url_for('auth.login'))
