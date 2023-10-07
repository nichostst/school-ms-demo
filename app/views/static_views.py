# Standard Library imports

# Core Flask imports
from flask import render_template, redirect
from flask_login import login_required, current_user

# Third-party imports

# App imports
from ..permissions import roles_required
from .. import db_manager as db
from ..models import Role, User, Module, Term, modules_coordinators, modules_lecturers
from ..utils.tables.admin import get_user_table_html, get_module_table_html

# Declare type
current_user: User


def index():
    return render_template('index.html')

def register():
    return render_template('register.html')

def login():
    return render_template('login.html')

# Common login-required views
@login_required
def home():
    role: Role = current_user.role
    return redirect(f'{role.name}')

@login_required
def profile():
    return render_template('profile.html')

# Admin only views

@login_required
@roles_required('admin')
def admin():
    # User table
    user_table = get_user_table_html(session=db.session)
    module_table = get_module_table_html(session=db.session)
    tables = {
        'user': user_table,
        'module': module_table
    }
    
    return render_template(
        'admin/admin.html',
        tables=tables,
        current_user=current_user
    )

@login_required
@roles_required('admin')
def new_user():
    roles = db.session.query(Role).all()
    return render_template('admin/new_user.html', roles=roles)

@login_required
@roles_required('admin')
def new_module():
    coordinators = db.session.query(User).join(User.role).filter(Role.name == 'coordinator').all()
    lecturers = db.session.query(User).join(User.role).filter(Role.name == 'lecturer').all()
    return render_template('admin/new_module.html', coordinators=coordinators, lecturers=lecturers)

# Coordinator only views

@login_required
@roles_required('coordinator')
def coordinator():
    module_list = db.session.query(Module).all()
    module_names = {m.module_id: m.name for m in module_list}

    lecturer_list = db.session.query(User).join(User.role).filter(Role.name == 'lecturer').all()
    lecturer_names = {l.user_id: l.username for l in lecturer_list}

    term_list = db.session.query(Term).all()
    term_names = {t.term_id: t.name for t in term_list}

    mc = db.session.query(
        modules_coordinators.c.coordinator_id,
        modules_coordinators.c.module_id,
    ).filter(modules_coordinators.c.coordinator_id == current_user.user_id).all()
    modules = [m.module_id for m in mc]

    module_lecturers_list = db.session.query(
        modules_lecturers.c.lecturer_id,
        modules_lecturers.c.module_id,
        modules_lecturers.c.term_id,
    ).all()

    module_lecturers_terms = []
    for m in modules:
        for ml in module_lecturers_list:
            if ml.module_id == m:
                module_lecturers_terms.append({
                    'module_id': m,
                    'module_name': module_names[m],
                    'lecturer': lecturer_names[ml.lecturer_id],
                    'term': term_names[1]
                })

    return render_template('coordinator/coordinator.html')
