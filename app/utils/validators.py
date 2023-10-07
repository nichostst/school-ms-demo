# Standard Library imports

# Core Flask imports

# Third-party imports
from marshmallow import Schema, fields, validate

# App imports


class AccountValidator(Schema):
    username = fields.Str(
        required=True,
        load_only=True,
        validate=[
            validate.Length(
                1, 15, error="Username must be at most 15 characters."
            ),
            validate.Regexp(
                "^[a-zA-Z][a-zA-Z0-9_]*$",
                error="Username must start with a letter, and contain only letters, numbers, and underscores."
            )
        ]
    )
    email = fields.Email(required=True, load_only=True)
    password = fields.Str(required=True, load_only=True)

class EmailValidator(Schema):
    email = fields.Email(required=True, load_only=True)

class ModuleValidator(Schema):
    module_code = fields.Str(
        required=True,
        load_only=True,
        validate=[
            validate.Length(5, 6, error="Length of module code has to be 5 or 6."),
            validate.Regexp(
                "[A-Z]{2}[0-9]{3,4}",
                error="Module code has to start with two capital letters followed by 3 to 4 numbers."
            )
        ]
    )
    credits = fields.Integer(
        required=True,
        load_only=True,
        validate=validate.Range(
            min=1, max=10, error="Value must be greater than 0 and at most 10."
        )
    )

    n_coordinators = fields.Integer(
        validate=validate.Range(
            min=1, max=2, error="At least one and at most 2 coordinator has to be selected."
        )
    )

    n_lecturers = fields.Integer(
        validate=validate.Range(
            min=1, max=4, error="At least one and at most 4 lecturer has to be selected."
        )
    )
