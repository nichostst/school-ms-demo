import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".flaskenv"))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SESSION_COOKIE_HTTPONLY = os.environ.get("SESSION_COOKIE_HTTPONLY")
    REMEMBER_COOKIE_HTTPONLY = os.environ.get("REMEMBER_COOKIE_HTTPONLY")
    SESSION_COOKIE_SAMESITE = os.environ.get("SESSION_COOKIE_SAMESITE")


class DevelopmentConfig(Config):
    SQLALCHEMY_DB_URI = os.environ.get('DEV_DB_URI')

class TestingConfig(Config):
    TESTING = True


config_manager = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
}