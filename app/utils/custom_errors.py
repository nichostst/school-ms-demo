# Standard Library imports

# Core Flask imports

# Third-party imports
from sqlalchemy.exc import SQLAlchemyError

# App imports


class Error(Exception):
    message = "Error"
    internal_error_code = 99999

    def __init__(self, value=""):
        if not hasattr(self, "value"):
            self.value = value

    def __str__(self):
        return repr(self.value)


class EmailAlreadyExistsError(Error):
    message = "There is already an account associated with this email address."
    internal_error_code = 40902

class InternalDBError(Error, SQLAlchemyError):
    message = "Sorry, we had a problem with that request. Please try again later or contact customer support."
    internal_error_code = 50001

class CouldNotVerifyLogin(Error):
    message = "Login failed."
    internal_error_code = 40101

class PermissionDeniedError(Error):
    message = "You don't have necessary permissions."
    internal_error_code = 40301

class ModuleAlreadyExistsError(Error):
    message = "There is already an module associated with this module code."
    internal_error_code = 40903
