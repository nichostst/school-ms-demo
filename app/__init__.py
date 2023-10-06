# Standard Library imports
import logging
from logging.handlers import RotatingFileHandler
import os

# Core Flask imports
from flask import Flask
from flask_login import LoginManager

# Third-party imports

# App imports
from app.routes import init_routes
from app.database import DatabaseManager
from config import config_manager


# Load extensions
db_manager = DatabaseManager()
login_manager = LoginManager()


def create_app(env):
    '''
    Create Flask app with app factory pattern method. Client component

    :param env: Either dev/test/prod
    '''
    app = Flask(__name__)
    app.config.from_object(config_manager[env])

    db_manager.init_app(app)

    login_manager.login_view = 'login'
    login_manager.init_app(app)

    init_routes(app, db=db_manager.session)

    return app
