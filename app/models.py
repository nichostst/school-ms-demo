# Standard Library imports

# Core Flask imports
from flask_login import UserMixin

# Third-party imports
from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    Text,
    String,
    Boolean,
    DateTime,
    ForeignKey,
)
from sqlalchemy import func as F
from sqlalchemy.orm import relationship

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
    confirmed = Column(Boolean, nullable=False, server_default="false")

    account_id = Column(Integer, ForeignKey('accounts.account_id'), nullable=False)

    account = relationship('Account', back_populates='users')
    role = relationship('Role', uselist=False, secondary='users_roles')

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

class ModuleCoordinator(Base):
    __tablename__ = 'modules_coordinators'
    coordinator_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    module_id = Column(Integer, ForeignKey("modules.module_id"), primary_key=True)
    assigned_at = Column(DateTime, nullable=False, server_default=F.now())

class ModuleLecturer(Base):
    __tablename__ = 'modules_lecturers'
    coordinator_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    module_id = Column(Integer, ForeignKey("modules.module_id"), primary_key=True)
    assigned_at = Column(DateTime, nullable=False, server_default=F.now())

class ModuleStudents(Base):
    __tablename__ = 'modules_students'
    coordinator_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    module_id = Column(Integer, ForeignKey("modules.module_id"), primary_key=True)
    term_id = Column(Integer, ForeignKey("terms.term_id"), nullable=False)
    grade = Column(Numeric)
    assigned_at = Column(DateTime, nullable=False, server_default=F.now())

class ModuleGradeStructure(Base):
    __tablename__ = 'module_grade_structure'
    module_id = Column(Integer, ForeignKey("modules.module_id"), primary_key=True)
    structure_type = Column(Text, nullable=False)
    weightage = Column(Numeric, nullable=False)

class Term(Base):
    __tablename__ = 'terms'
    term_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
