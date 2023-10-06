# Standard Library imports
from typing import List

# Core Flask imports

# Third-party imports

# App imports
from app.models import User
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
