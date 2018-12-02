# -*- coding: utf-8 -*-

from functools import wraps
from flask_login import current_user
from webapp import login

ADMIN = "admin"
BOSS = "boss"
USER = "user"
ANY = "ANY"

roles_arr = [(ADMIN, ADMIN), (BOSS, BOSS), (USER, USER)]

def login_required(roles=["ANY"]):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return login.unauthorized()
            access_granted = False
            if roles[0] != "ANY":
                for checked_role in roles:
                    if current_user.role == checked_role:
                        access_granted = True
                        break
                if not access_granted:
                    return login.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper