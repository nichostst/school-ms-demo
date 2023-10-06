# Standard Library imports

# Core Flask imports
from flask import request, redirect, url_for
from flask_login import login_user, logout_user

# Third-party imports
import marshmallow

# App imports
from app import db_manager as db
from ..models import User, Account
from ..services import account_management_services as am
from ..utils import custom_errors, sanitization
from ..utils.validators import AccountValidator
from ..utils.error_utils import (
    get_business_requirement_error_response,
    get_validation_error_response,
    get_db_error_response
)

def _register_account():
    unsafe_username = request.json.get('username')
    unsafe_email = request.json.get('email')
    unhashed_password = request.json.get('password')

    username = sanitization.strip_xss(unsafe_username)
    email = sanitization.strip_xss(unsafe_email)

    try:
        user_model = am.create_account(username, email, unhashed_password)
    except marshmallow.ValidationError as e:
        return get_validation_error_response(validation_error=e, http_status_code=422)
    except custom_errors.EmailAlreadyExistsError as e:
        return get_business_requirement_error_response(logic_error=e, http_status_code=409)
    except custom_errors.InternalDBError as e:
        return get_db_error_response(db_error=e, http_status_code=500)
    
    return user_model

def register_account():
    user_model = _register_account()
    login_user(user_model, remember=True)

    return {'message': 'Success'}, 201


def admin_register_account():
    user_model = _register_account()

    role = request.json.get('role')
    am.assign_role(user_model, role)

    return {'message': 'Success'}, 201


def login_account():
    unsafe_email = request.json.get('email')
    unhashed_password = request.json.get('password')

    email = sanitization.strip_xss(unsafe_email)

    try:
        user_model = am.verify_login(email, unhashed_password)
    except marshmallow.ValidationError as e:
        return get_validation_error_response(validation_error=e, http_status_code=422)
    except custom_errors.CouldNotVerifyLogin as e:
        return get_business_requirement_error_response(logic_error=e, http_status_code=401)

    login_user(user_model, remember=True)

    return {'success': 'True'}, 200

def logout_account():
    logout_user()
    return redirect(url_for('index'))
