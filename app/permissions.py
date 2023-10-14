# Standard Library imports
from functools import wraps

# Core Flask imports
from flask_login import current_user

# Third-party imports

# App imports
from .utils.error_utils import get_business_requirement_error_response
from .utils.custom_errors import PermissionDeniedError
from .models import modules_coordinators
from . import db_manager as db

def roles_required(role):
    def decorated_function(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if role == current_user.role.name:
                return f(*args, **kwargs)
            else:
                return get_business_requirement_error_response(PermissionDeniedError, 403)
        return wrapper
    return decorated_function

def coordinator_scope(module_id):
    coordinator_id = current_user.user_id
    query = db.session.query(
        modules_coordinators.c.coordinator_id,
        modules_coordinators.c.module_id
    ).filter(
        modules_coordinators.c.coordinator_id == coordinator_id
    ).all()

    modules_coordinated = [q.module_id for q in query]

    if module_id in modules_coordinated:
        return True
    else:
        return False
