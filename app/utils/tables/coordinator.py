# Standard Library imports
from collections import defaultdict

# Core Flask imports
from flask_login import current_user

# Third-party imports
from sqlalchemy.orm import scoped_session

# App imports
from app.models import (
    User, Module, Term, Role, ModuleGradeStructure,
    modules_coordinators, modules_lecturers
)
from app.utils.html.table import Tabulator
from app.utils.html.elements import MaterialDropdown


def _get_module_names_codes(session: scoped_session):
    module_list = session.query(Module).all()
    module_names = {m.module_id: m.name for m in module_list}
    module_codes = {m.module_id: m.module_code for m in module_list}
    return module_names, module_codes

def _get_coordinated_modules(session: scoped_session):
    mc = session.query(
        modules_coordinators.c.coordinator_id,
        modules_coordinators.c.module_id,
    ).filter(modules_coordinators.c.coordinator_id == current_user.user_id).all()
    coordinated_modules = [m.module_id for m in mc]
    return coordinated_modules

def get_modules_lecturers_table_html(session: scoped_session, assign_terms=False):
    module_names, module_codes = _get_module_names_codes(session)

    # Map lecturer ID to lecturer names
    lecturer_list = session.query(User).join(User.role).filter(Role.name == 'lecturer').all()
    lecturer_names = {l.user_id: l.username for l in lecturer_list}

    # Map term ID to term names
    term_list = session.query(Term).all()
    term_names = {t.term_id: t.name for t in term_list}

    # Query all modules coordinated by current user
    coordinated_modules = _get_coordinated_modules(session)

    # All module-lecturer-term relationships under current user
    module_lecturers_list = session.query(
        modules_lecturers.c.lecturer_id,
        modules_lecturers.c.module_id,
        modules_lecturers.c.term_id,
    ).filter(
        modules_lecturers.c.module_id.in_(coordinated_modules)
    ).all()

    # All pair of module-lecturers with list of terms assigned
    module_lecturer_pairs = {(ml.module_id, ml.lecturer_id): [] for ml in module_lecturers_list}
    for ml in module_lecturers_list:
        if ml.term_id:
            module_lecturer_pairs[(ml.module_id, ml.lecturer_id)].append(ml.term_id)

    # All modules with terms assigned
    module_terms_assigned = {ml.module_id: [] for ml in module_lecturers_list}
    for ml in module_lecturers_list:
        if ml.term_id:
            module_terms_assigned[ml.module_id].append(ml.term_id)

    # Build table to display
    module_lecturers_terms = []
    for (module_id, lecturer_id), term_ids in module_lecturer_pairs.items():
        if assign_terms:
            valid_terms = {
                term_id: term_name for term_id, term_name in term_names.items()
                if term_id not in module_terms_assigned[module_id]
            }
            term_section = MaterialDropdown(
                options=valid_terms,
                name=f'dropdown-{ml.module_id}-{ml.lecturer_id}'
            ).html()

        elif term_ids:
            term_section = ', '.join([term_names[tid] for tid in term_ids])
        else:
            term_section = '<em style="font-style: italic; font-weight: lighter;">Unassigned</em>'

        module_lecturers_terms.append({
            'module_code': module_codes[module_id],
            'module_name': module_names[module_id],
            'lecturer': lecturer_names[lecturer_id],
            'term': term_section
        })
        

    cols = ['module_code', 'module_name', 'lecturer', 'term']
    col_labels = ['Module Code', 'Module Name', 'Lecturer', 'Term']
    styles = ['compact', 'stripe', 'hover']

    tab = Tabulator()
    modules_lecturers_table_html = tab.tabulate(
        data=module_lecturers_terms,
        cols=cols,
        col_labels=col_labels,
        alias='modules_lecturers',
        styles=styles)
    return modules_lecturers_table_html

def get_grade_structure_table_html(session: scoped_session):
    module_names, module_codes = _get_module_names_codes(session)
    coordinated_modules = _get_coordinated_modules(session)

    grade_structure = session.query(ModuleGradeStructure).all()

    grade_structure_table = []
    for m in coordinated_modules:
        module_structure = [g for g in grade_structure if g.module_id == m]
        structure = []
        for ms in module_structure:
            structure.append(f'{ms.structure_type.capitalize()}: {ms.weightage:.2f}')
        
        if module_structure:
            structure_html = "<br>".join(structure)
        else:
            structure_html = '<em style="font-style: italic; font-weight: lighter; font-size: 14px;">Empty</em>'

        structure_section = f'''
            <div>
                <div style="display: inline-block; vertical-align: middle; width: 60%;">
                    {structure_html}
                </div>
                <div style="display: inline-block; vertical-align: middle; margin: 10pt">
                    <a href="/coordinator/grade_restructure/{m}">
                        <span class="material-icons">edit</span>
                    </a>
                </div>
            </div>
        '''

        grade_structure_table.append({
            'module_code': module_codes[m],
            'module_name': module_names[m],
            'structure': structure_section,
        })

    cols = ['module_code', 'module_name', 'structure']
    col_labels = ['Module Code', 'Module Name', 'Structure']
    styles = ['compact', 'stripe', 'hover']

    tab = Tabulator()
    grade_structure_table_html = tab.tabulate(
        data=grade_structure_table,
        cols=cols,
        col_labels=col_labels,
        alias='modules_lecturers',
        styles=styles
    )
    return grade_structure_table_html