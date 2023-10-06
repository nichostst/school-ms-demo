# Standard Library imports

# Core Flask imports
from flask import render_template, url_for, redirect
from flask_login import login_required, current_user

# Third-party imports
from sqlalchemy import select

# App imports
from ..permissions import roles_required
from .. import db_manager as db
from ..models import User, Role
from ..utils.html.table import Tabulator

def index():
    return render_template('index.html')

def register():
    return render_template('register.html')

def login():
    return render_template('login.html')

@login_required
def home():
    return redirect(f'{current_user.role.name}')

@login_required
def profile():
    return render_template('profile.html')

@login_required
@roles_required('admin')
def admin():
    # User table
    users = db.session.query(User).all()
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
    user_table = tab.tabulate(data=data, cols=cols, col_labels=col_labels, alias='user', styles=styles)
    return render_template('admin.html', user_table=user_table, current_user=current_user)

@login_required
@roles_required('admin')
def new_user():
    roles = db.session.query(Role).all()
    return render_template('new_user.html', roles=roles)
