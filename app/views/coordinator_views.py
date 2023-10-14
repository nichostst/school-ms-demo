# Standard Library imports

# Core Flask imports
from flask import render_template, request, url_for, redirect
from flask_login import login_required

# Third-party imports

# App imports
from ..permissions import roles_required, coordinator_scope
from .. import db_manager as db
from ..models import User
from ..utils.tables.coordinator import (
    get_modules_lecturers_table_html,
    get_grade_structure_table_html,
    get_grade_restructure_interface_html,
    get_create_structure_interface_html,
    get_module_code
)
from ..services import coordinator_services as cs

# Declare type
current_user: User


@login_required
@roles_required('coordinator')
def coordinator():
    tables = _coordinator_tables()
    restructure_success = request.args.get('restructure_success')
    return render_template(
        'coordinator/coordinator.html',
        tables=tables,
        restructure_success=restructure_success
    )

@login_required
@roles_required('coordinator')
def coordinator_restructure_success():
    return redirect(url_for('coordinator', restructure_success=True))

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
def grade_restructure(module_id):
    if not coordinator_scope(module_id):
        return render_template('404.html')

    module_code = get_module_code(session=db.session, module_id=module_id)
    grade_restructure_interface = get_grade_restructure_interface_html(
        session=db.session, module_id=module_id, input_=False
    )
    grade_restructure_input = get_grade_restructure_interface_html(
        session=db.session, module_id=module_id, input_=True
    )

    tables = {
        'grade_restructure_interface': grade_restructure_interface,
        'grade_restructure_input': grade_restructure_input
    }

    return render_template('coordinator/grade_restructure.html', tables=tables, module_code=module_code)

@login_required
@roles_required('coordinator')
def create_structure(module_id):
    if not coordinator_scope(module_id):
        return render_template('404.html')

    module_code = get_module_code(session=db.session, module_id=module_id)
    create_structure_interface = get_create_structure_interface_html(
        session=db.session, module_id=module_id
    )

    tables = {
        'create_structure_interface': create_structure_interface
    }

    return render_template('coordinator/create_structure.html', tables=tables, module_code=module_code)

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

@login_required
@roles_required('coordinator')
def restructure_api():
    new_structures = request.json.get('new_structures')
    new_weights = {
        s['structure_id']: int(s['structure_weight'])/100
        for s in new_structures
    }

    result = cs.change_weights(new_weights)
    redirect_to = url_for('coordinator') + '/restructure_success'
    if result == 'success':
        return {'message': 'Success', 'result': result, 'redirect_to': redirect_to}, 201
    else:
        return {'message': 'Unsuccessful', 'result': result}, 412

def _coordinator_tables():
    modules_lecturers_table = get_modules_lecturers_table_html(session=db.session)
    grade_structure_table = get_grade_structure_table_html(session=db.session)
    tables = {
        'modules_lecturers': modules_lecturers_table,
        'grade_structure': grade_structure_table,
    }
    return tables