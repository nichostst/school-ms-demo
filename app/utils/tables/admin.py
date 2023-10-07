# Standard Library imports
from typing import List

# Core Flask imports

# Third-party imports
from sqlalchemy.orm import scoped_session

# App imports
from app.models import User, Module, ModuleCoordinator, ModuleLecturer
from app.utils.html.table import Tabulator


def get_user_table_html(session):
    users: List[User] = session.query(User).all()

    data = [
        {
            'user_id': u.user_id,
            'username': u.username,
            'email': u.email,
            'role': u.role.name,
            'created_at': u.created_at
        } for u in users
    ]
    cols = ['user_id', 'username', 'email', 'role', 'created_at']
    col_labels = ['ID', 'Username', 'Email', 'Role', 'Created At']
    styles = ['compact', 'stripe', 'hover']

    tab = Tabulator()
    user_table_html = tab.tabulate(data=data, cols=cols, col_labels=col_labels, alias='user', styles=styles)
    return user_table_html

def get_module_table_html(session):
    modules: List[Module] = session.query(Module).all()
    module_ids = [m.module_id for m in modules]

    coordinators: List[ModuleCoordinator] = session.query(ModuleCoordinator).all()
    lecturers: List[ModuleLecturer] = session.query(ModuleLecturer).all()

    users: List[User] = session.query(User).all()
    id_to_username = {u.user_id: u.username for u in users}

    module_coordinators = {
        m: [id_to_username[c.coordinator_id] for c in coordinators if c.module_id == m]
        for m in module_ids
    }
    module_lecturers = {
        m: [id_to_username[l.lecturer_id] for l in lecturers if l.module_id == m]
        for m in module_ids
    }

    data = [
        {
            'module_id': m.module_id,
            'module_code': m.module_code,
            'module_name': m.name,
            'credits': m.credits,
            'coordinators': ', '.join(module_coordinators[m.module_id]),
            'lecturers': ', '.join(module_lecturers[m.module_id]),
        } for m in modules
    ]
    print(data)
    cols = ['module_id', 'module_code', 'module_name', 'credits', 'coordinators', 'lecturers']
    col_labels = ['ID', 'Code', 'Name', 'Credits', 'Coordinators', 'Lecturers']
    styles = ['compact', 'stripe', 'hover']

    tab = Tabulator()
    module_table_html = tab.tabulate(data=data, cols=cols, col_labels=col_labels, alias='module', styles=styles)
    return module_table_html
