from functools import wraps
from flask_login import current_user
from flask import abort, redirect, url_for


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