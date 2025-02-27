import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24).hex())
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db/postgres')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', os.urandom(24).hex())
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_EXPIRATION', 3600))
    JWT_COOKIE_CSRF_PROTECT =os.getenv('JWT_COOKIE_CSRF_PROTECT', False) 
    JWT_ACCESS_COOKIE_NAME = os.getenv('JWT_ACCESS_COOKIE_NAME', 'jwt_token')
    JWT_TOKEN_LOCATION=os.getenv('JWT_TOKEN_LOCATION', ["cookies"])
    DEBUG = str(os.getenv('DEBUG', 'False')).lower() in ['true', '1']

    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
    LOG_LEVEL = 'INFO'
    LOG_MAX_BYTES = int(os.getenv('LOG_MAX_BYTES', 100000))
    LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', 3))
