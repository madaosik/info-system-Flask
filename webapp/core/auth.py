# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from functools import wraps
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Email, DataRequired, EqualTo, ValidationError
from flask_login import current_user

from webapp.core import db
from webapp import login

class LoginForm(FlaskForm):
    login = StringField('Uživatelské jméno',validators=[InputRequired(message="Zadejte uživatelské jméno!")])
    password = PasswordField('Heslo', validators=[InputRequired(message="Zadejte heslo!")])
    remember_me = BooleanField('Pamatuj si mě')
    submit = SubmitField('Přihlásit se')

class RegistrationForm(FlaskForm):
    login = StringField('Uživatelské jméno', validators=[DataRequired(message="Zadejte uživatelské jméno")])
    email = StringField('E-mail', validators=[DataRequired(),Email(message="Nepovolený tvar e-mailové adresy!")])
    password = PasswordField('Heslo', validators=[DataRequired(message="Zadejte heslo!")])
    password2 = PasswordField('Zopakování hesla', validators=[DataRequired(), EqualTo('password',message="Zadaná hesla se neshodují!")])
    submit = SubmitField('Registrace')

    def validate_username(self, login):
        user = db.get_user_by_login(login=login.data)
        if user is not None:
            raise ValidationError('Použijte, prosím, jiné uživatelské jméno!')

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