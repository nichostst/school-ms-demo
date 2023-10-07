# Standard Library imports

# Core Flask imports

# Third-party imports

# App imports
from app import db_manager as db
from ..models import  Module, modules_coordinators, modules_lecturers
from ..utils.validators import ModuleValidator
from ..utils import custom_errors


def create_module(module_code, module_name, credits, coordinators, lecturers):
    fields_to_validate_dict = {
        "module_code": module_code,
        "credits": int(credits),
        "n_coordinators": len(coordinators),
        "n_lecturers": len(lecturers)
    }

    ModuleValidator().load(fields_to_validate_dict)

    if (
        db.session.query(Module.module_code).filter_by(module_code=module_code).first()
    ) is not None:
        raise custom_errors.ModuleAlreadyExistsError()

    module_model = Module(
        module_code=module_code,
        name=module_name,
        credits=credits
    )
    db.session.add(module_model)
    db.session.flush()

    for c in coordinators:
        mc = modules_coordinators.insert().values(
            coordinator_id=c,
            module_id=module_model.module_id
        )
        db.session.execute(mc)

    for l in lecturers:
        ml = modules_lecturers.insert().values(
            lecturer_id=l,
            module_id=module_model.module_id,
            term_id=None
        )
        db.session.execute(ml)

    db.session.commit()

    return module_model
