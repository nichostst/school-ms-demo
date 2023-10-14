# Standard Library imports

# Core Flask imports
from flask import render_template, redirect
from flask_login import login_required, current_user

# Third-party imports

# App imports
from ..models import Role, User

# Declare type
current_user: User


def index():
    return render_template('index.html')

def login():
    if current_user.is_active:
        return home()
    else:
        return render_template('login.html')

# Common login-required views
@login_required
def home():
    role: Role = current_user.role
    return redirect(f'{role.name}')

@login_required
def profile():
    return render_template('profile.html')
