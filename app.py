import logging
import os
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from models import db
from config import Config
from routes.auth import auth_bp
from routes.tasks import tasks_bp
from routes.home import home_bp
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
csrf = CSRFProtect()
csrf.init_app(app)

csrf.exempt("tasks_bp")#se function name from Blueprint


app.register_blueprint(home_bp, url_prefix='/')
app.register_blueprint(tasks_bp, url_prefix='/tasks')
app.register_blueprint(auth_bp, url_prefix='/auth')

if not os.path.exists("logs"):
    os.makedirs("logs")

log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

if app.logger.hasHandlers():
    app.logger.handlers.clear()

print(Config.DEBUG, 'Config.DEBUG')

if Config.DEBUG:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(console_handler)
else:
    file_handler = RotatingFileHandler(
        Config.LOG_FILE, maxBytes=Config.LOG_MAX_BYTES, backupCount=Config.LOG_BACKUP_COUNT
    )
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)

app.logger.setLevel(logging.DEBUG)
logging.getLogger().handlers = app.logger.handlers

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=Config.DEBUG)
