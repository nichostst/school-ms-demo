# Standard Library imports
from typing import List

# Core Flask imports
from flask_login import UserMixin

# Third-party imports
from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    Text,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy import func as F
from sqlalchemy import Table
from sqlalchemy.orm import relationship, Mapped

# App imports
from app import db_manager

# Alias
Base = db_manager.base


class Account(Base):
    __tablename__ = 'accounts'
    account_id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=F.now())

    users = relationship('User', back_populates='account')


class User(Base, UserMixin):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(Text, unique=True)
    email = Column(Text, unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=F.now())

    account_id = Column(Integer, ForeignKey('accounts.account_id'), nullable=False)

    account = relationship('Account', back_populates='users')
    role = relationship('Role', uselist=False, secondary='users_roles')

    coordinated_modules = relationship(
        'Module', uselist=False, secondary='modules_coordinators', back_populates='coordinators'
    )
    taught_modules = relationship(
        'Module', uselist=False, secondary='modules_lecturers', back_populates='lecturers'
    )

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return f'<User {self.email}>'

class Role(Base):
    __tablename__ = 'roles'
    role_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)

    def __repr__(self):
        return f"<Role {self.name}>"

class UserRole(Base):
    __tablename__ = 'users_roles'
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.role_id"), primary_key=True)
    assigned_at = Column(DateTime, nullable=False, server_default=F.now())

class Module(Base):
    __tablename__ = 'modules'
    module_id = Column(Integer, primary_key=True)
    module_code = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    credits = Column(Integer)

    coordinators = relationship(
        'User', uselist=False, secondary='modules_coordinators', back_populates='coordinated_modules'
    )
    lecturers = relationship(
        'User', uselist=False, secondary='modules_lecturers', back_populates='taught_modules'
    )

modules_coordinators = Table('modules_coordinators', Base.metadata,
    Column('coordinator_id', Integer, ForeignKey('users.user_id'), primary_key=True),
    Column('module_id', Integer, ForeignKey('modules.module_id'), primary_key=True)
)

modules_lecturers = Table('modules_lecturers', Base.metadata,
    Column('lecturer_id', Integer, ForeignKey('users.user_id'), primary_key=True),
    Column('module_id', Integer, ForeignKey('modules.module_id'), primary_key=True),
    Column('term_id', Integer, ForeignKey('terms.term_id')),
)

modules_students = Table('modules_students', Base.metadata,
    Column('student_id', Integer, ForeignKey('users.user_id'), primary_key=True),
    Column('module_id', Integer, ForeignKey('modules.module_id'), primary_key=True),
    Column('term_id', Integer, ForeignKey('terms.term_id')),
    Column('grade', Numeric),
)

class ModuleGradeStructure(Base):
    __tablename__ = 'module_grade_structure'
    structure_id = Column(Integer, primary_key=True)
    module_id = Column(Integer, ForeignKey("modules.module_id"), nullable=False)
    structure_type = Column(Text, nullable=False)
    weightage = Column(Numeric, nullable=False)

class Term(Base):
    __tablename__ = 'terms'
    term_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
