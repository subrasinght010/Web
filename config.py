import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db/postgres')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwtsecretkey')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_EXPIRATION', 3600))

    DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1']

    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
    LOG_LEVEL = 'INFO'
    LOG_MAX_BYTES = int(os.getenv('LOG_MAX_BYTES', 100000))
    LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', 3))
