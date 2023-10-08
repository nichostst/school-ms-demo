# Standard Library imports

# Core Flask imports
from flask import render_template, request
from flask_login import login_required

# Third-party imports

# App imports
from ..permissions import roles_required
from .. import db_manager as db
from ..models import User
from ..utils.tables.coordinator import get_modules_lecturers_table_html
from ..services import coordinator_services as cs

# Declare type
current_user: User


@login_required
@roles_required('coordinator')
def coordinator():
    modules_lecturers_table = get_modules_lecturers_table_html(session=db.session)
    tables = {
        'modules_lecturers': modules_lecturers_table,
    }
    return render_template('coordinator/coordinator.html', tables=tables)

@login_required
@roles_required('coordinator')
def assign_lecturer():
    modules_lecturers_table = get_modules_lecturers_table_html(session=db.session, assign_terms=True)
    tables = {
        'modules_lecturers': modules_lecturers_table,
    }
    return render_template('coordinator/assign_lecturer.html', tables=tables)

@login_required
@roles_required('coordinator')
def assign_api():
    id_value = request.json.get('id_value')

    valid_input = True
    module_term_pair = []
    for dropdown_id, term_ids in id_value:
        module_id, lecturer_id = dropdown_id.split('-')[1:]
        term_ids = [int(t) for t in term_ids]
        for t in term_ids:
            key = (module_id, t)
            if key not in module_term_pair:
                module_term_pair.append(key)
            else:
                print('Input invalid!')
                valid_input = False

    if valid_input:
        for dropdown_id, term_ids in id_value:
            module_id, lecturer_id = dropdown_id.split('-')[1:]
            term_ids = [int(t) for t in term_ids]
            result = cs.assign_lecturer(int(module_id), int(lecturer_id), term_ids)

        if result == 'success':
            return {'message': 'Success', 'result': result}, 201
        else:
            return {'message': 'Partially successful', 'result': result}, 201
    else:
        return {'message': 'Unsuccessful', 'result': 'failure'}, 412
