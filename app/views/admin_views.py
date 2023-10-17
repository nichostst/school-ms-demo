# Standard Library imports

# Core Flask imports
from flask import render_template
from flask_login import login_required, current_user

# Third-party imports

# App imports
from ..permissions import roles_required
from .. import db_manager as db
from ..models import Role, User
from ..utils.tables.admin import get_user_table_html, get_module_table_html, get_role_counts

# Declare type
current_user: User


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

    role_counts = get_role_counts(session=db.session)
    
    return render_template(
        'admin/admin.html',
        tables=tables,
        current_user=current_user,
        role_counts=role_counts
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
