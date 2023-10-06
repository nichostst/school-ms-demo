# Standard Library imports
from functools import wraps

# Core Flask imports
from flask_login import current_user

# Third-party imports

# App imports
from .utils.error_utils import get_business_requirement_error_response
from .utils.custom_errors import PermissionDeniedError


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
