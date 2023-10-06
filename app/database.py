# Standard Library imports

# Core Flask imports
from flask import Flask

# Third-party imports
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import (
    scoped_session, sessionmaker, declarative_base, QueryPropertyDescriptor
)

# App imports

# Load extensions


class DatabaseManager():
    def __init__(self, app: Flask = None):
        self.app    : Flask          = app
        self.session: scoped_session = None
        self.engine : Engine         = None
        self.base                    = declarative_base()

    def init_app(self, app):
        self.create_engine(app.config['SQLALCHEMY_DB_URI'])

        self.create_scoped_session()

        self.base.query: QueryPropertyDescriptor = self.session.query_property()

    def create_engine(self, sqlalchemy_db_uri):
        self.engine = create_engine(sqlalchemy_db_uri)

    def create_scoped_session(self):
        self.session = scoped_session(sessionmaker(bind=self.engine))
