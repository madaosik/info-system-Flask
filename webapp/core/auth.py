# -*- coding: utf-8 -*-

from functools import wraps
from flask import redirect, url_for, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired
from flask_login import current_user, login_user, logout_user

from webapp.core import db

class LoginForm(FlaskForm):
    login = StringField('Uživatelské jméno',validators=[InputRequired(message="Zadejte uživatelské jméno!")])
    password = PasswordField('Heslo', validators=[InputRequired(message="Zadejte heslo!")])
    remember_me = BooleanField('Pamatuj si mě')
    submit = SubmitField('Přihlásit se')


# def login_required(roles=["ANY"]):
#     def wrapper(fn):
#         @wraps(fn)
#         def decorated_view(*args, **kwargs):
#             if not current_user.is_authenticated:
#                 return login_manager.unauthorized()
#             access_granted = False
#             if roles[0] != "ANY":
#                 for checked_role in roles:
#                     if current_user.role == checked_role:
#                         access_granted = True
#                         break
#                 if not access_granted:
#                     return login_manager.unauthorized()
#             return fn(*args, **kwargs)
#         return decorated_view
#     return wrapper

def configure_login(app):
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('home'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        error = None
        if current_user.is_authenticated:
            if current_user.is_employee():
                return redirect(url_for('dashboard_empl'))
            else:
                return redirect(url_for('dashboard_boss'))
        form = LoginForm()
        if form.validate_on_submit():
            user = db.get_user_by_attr(login=form.login.data)
            if user is None:
                error = "Neznámé uživatelské jméno!"
            elif not user.check_password(form.password.data):
                error = "Neplatné heslo!"
            else:
                login_user(user, remember=form.remember_me.data)
                db.log_visit(user)
                flash("Přihlášení proběhlo úspěšně!", 'alert-success')
                if user.is_employee():
                    print("cus")
                    return redirect(url_for('dashboard_empl'))
                else:
                    print("zdar")
                    return redirect(url_for('dashboard_boss'))
        return render_template('login.html', title='Přihlášení', form=form, error=error)
