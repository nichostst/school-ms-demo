# Standard Library imports

# Core Flask imports
from flask import Flask, render_template, redirect, url_for, request
from flask_login import login_user, current_user, login_required

# Third-party imports
from sqlalchemy.orm import scoped_session

# App imports


def init_routes(app: Flask, db: scoped_session) -> None:
    from .views import static_views, error_views, account_management_views
    from .models import User
    from app import login_manager

    @app.before_request
    def before_request():
        db()
    
    @app.teardown_appcontext
    def shutdown_session(response_or_exc):
        db.remove()
    
    @login_manager.user_loader
    def load_user(user_id):
        if user_id and user_id != 'None':
            return User.query.filter_by(user_id=user_id).first()

    # Public views
    app.add_url_rule('/', view_func=static_views.index)
    app.add_url_rule('/register', view_func=static_views.register)
    app.add_url_rule('/login', view_func=static_views.login)

    # Public APIs
    app.add_url_rule(
        '/api/register',
        view_func=account_management_views.register_account,
        methods=['POST']
    )
    app.add_url_rule(
        '/api/login',
        view_func=account_management_views.login_account,
        methods=['POST']
    )
    app.add_url_rule(
        '/logout',
        view_func=account_management_views.logout_account
    )

    # Admin APIs
    app.add_url_rule(
        '/api/admin/new_user',
        view_func=account_management_views.admin_register_account,
        methods=['POST']
    )

    # Login required views
    app.add_url_rule('/home', view_func=static_views.home)
    app.add_url_rule('/profile', view_func=static_views.profile)

    # Admin role required views
    app.add_url_rule('/admin', view_func=static_views.admin)
    app.add_url_rule('/admin/new_user', view_func=static_views.new_user)

    app.register_error_handler(404, error_views.not_found_error)
    app.register_error_handler(500, error_views.internal_error)
