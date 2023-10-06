# Standard Library imports

# Core Flask imports
from flask import request

# Third-party imports
import marshmallow

# App imports
from ..services import module_management_services as mm
from ..utils import custom_errors
from ..utils.error_utils import (
    get_business_requirement_error_response,
    get_validation_error_response,
    get_db_error_response
)

def admin_register_module():
    module_code = request.json.get('module_code')
    module_name = request.json.get('module_name')
    credits = request.json.get('credits')

    try:
        mm.create_module(module_code, module_name, credits)
    except marshmallow.ValidationError as e:
        return get_validation_error_response(validation_error=e, http_status_code=422)
    except custom_errors.EmailAlreadyExistsError as e:
        return get_business_requirement_error_response(logic_error=e, http_status_code=409)
    except custom_errors.InternalDBError as e:
        return get_db_error_response(db_error=e, http_status_code=500)

    return {'message': 'Success'}, 201