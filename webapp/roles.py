from functools import wraps
from flask_login import current_user
from flask import abort, redirect, url_for

roles = ['admin', 'user']

def get_role_tuples():
    roles_tuples_arr = []
    for role in roles:
        if role == 'admin':
            role_string = "Administrátor"
        elif role == 'user':
            role_string = "Zaměstnanec"
        elif role == 'boss':
            role_string = "Vedoucí"
        roles_tuples_arr.append((role,role_string))
    return roles_tuples_arr

def get_role_dict():
    roles_dict = {}
    for role in roles:
        if role == 'admin':
            roles_dict[role] = "Administrátor"
        elif role == 'user':
            roles_dict[role] = "Zaměstnanec"
        elif role == 'boss':
            roles_dict[role] = "Vedoucí"
    return roles_dict

# role decorators
def admin(func):
    @wraps(func)
    @login_required
    def _admin(*args, **kwargs):
        if current_user.is_admin():
            return func(*args, **kwargs)
        return abort(403)
    return _admin


def employee(func):
    @wraps(func)
    @login_required
    def _employee(*args, **kwargs):
        if current_user.is_employee():
            return func(*args, **kwargs)
        return abort(403)
    return _employee

def boss(func):
    @wraps(func)
    @login_required
    def _employee(*args, **kwargs):
        if current_user.is_boss():
            return func(*args, **kwargs)
        return abort(403)
    return _employee


def login_required(func):
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return decorated_view