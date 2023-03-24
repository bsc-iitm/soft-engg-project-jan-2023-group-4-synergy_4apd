import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLITE_DB_DIR = os.path.join(basedir, '../db_directory')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(SQLITE_DB_DIR, 'database.sqlite3')

    SECURITY_PASSWORD_HASH = None
    SECURITY_PASSWORD_SALT = None
    SECRET_KEY = None

    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False

    DEBUG = True