# Standard Library imports

# Core Flask imports
from flask import render_template, redirect
from flask_login import login_required, current_user

# Third-party imports

# App imports
from ..permissions import roles_required
from .. import db_manager as db
from ..models import Role
from ..utils.tables.admin import get_user_table_html, get_module_table_html

def index():
    return render_template('index.html')

def register():
    return render_template('register.html')

def login():
    return render_template('login.html')

@login_required
def home():
    role: Role = current_user.role
    return redirect(f'{role.name}')

@login_required
def profile():
    return render_template('profile.html')

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
    return render_template('admin/new_module.html')
