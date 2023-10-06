# Standard Library imports

# Core Flask imports

# Third-party imports
import bcrypt

# App imports
from app import db_manager as db
from ..models import User, Account, Role, UserRole
from ..utils.validators import AccountValidator, EmailValidator
from ..utils import custom_errors


def create_account(username, email, password: str):
    fields_to_validate_dict = {
        "username": username,
        "email": email,
        "password": password
    }

    AccountValidator().load(fields_to_validate_dict)

    if (
        db.session.query(User.email).filter_by(email=email).first()
    ) is not None:
        raise custom_errors.EmailAlreadyExistsError()

    hashed = bcrypt.hashpw(password.encode(), salt=bcrypt.gensalt())
    password_hash = hashed.decode()

    account_model = Account()
    db.session.add(account_model)
    db.session.flush()

    user_model = User(
        username=username,
        email=email,
        password_hash=password_hash,
        account_id=account_model.account_id
    )
    db.session.add(user_model)
    db.session.commit()

    return user_model

def verify_login(email, password: str):
    fields_to_validate_dict = {
        "email": email,
    }

    EmailValidator().load(fields_to_validate_dict)

    user_model = (
        db.session.query(User)
        .filter_by(email=email)
        .first()
    )
    
    if not user_model:
        raise custom_errors.CouldNotVerifyLogin()
    
    if not bcrypt.checkpw(password.encode(), user_model.password_hash.encode()):
        raise custom_errors.CouldNotVerifyLogin()
    
    return user_model

def assign_role(user_model: User, role: str):
    role = db.session.query(Role).filter_by(name=role).first()
    ur = UserRole(
        user_id=user_model.user_id,
        role_id=role.role_id
    )
    db.session.add(ur)
    db.session.commit()
