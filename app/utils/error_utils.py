# Standard Library imports

# Core Flask imports

# Third-party imports
from marshmallow import ValidationError

# App imports
from .custom_errors import Error


def get_validation_error_response(validation_error: ValidationError, http_status_code, display_error=""):
    resp = {
        "errors": {
            "display_error": display_error,
            "field_errors": validation_error.normalized_messages(),
        }
    }
    return resp, http_status_code

def get_business_requirement_error_response(logic_error: Error, http_status_code):
    resp = {
        "errors": {
            "display_error": logic_error.message,
            "internal_error_code": logic_error.internal_error_code,
        }
    }
    return resp, http_status_code

def get_db_error_response(db_error: Error, http_status_code):
    resp = {
        "errors": {
            "display_error": db_error.message,
            "internal_error_code": db_error.internal_error_code,
        }
    }
    return resp, http_status_code
