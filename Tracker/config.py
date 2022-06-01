from pathlib import Path
import os

BASEDIR = Path(__file__).parent


class BaseConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # WTF_CSRF_ENABLED = True
    SECRET_KEY = "c1bf717b3bc136aebebc"


class TestConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app_test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "c1bf717b3bc136aebebc"
    TESTING = True
    WTF_CSRF_ENABLED = False


