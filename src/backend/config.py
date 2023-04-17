from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()

class Config:
    SQLITE_DB_DIR = os.path.join(basedir, '../db_directory')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(SQLITE_DB_DIR, 'database.sqlite3')

    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'

    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')
    SECRET_KEY = os.getenv('SECRET_KEY')

    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False

    WTF_CSRF_ENABLED = False

    # Remember to turn off debug mode in production.
    DEBUG = True
