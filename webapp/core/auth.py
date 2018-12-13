# -*- coding: utf-8 -*-

from functools import wraps
from flask import redirect, url_for, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired
from flask_login import current_user, login_user, logout_user
from flask.views import MethodView

from webapp.core import db
from webapp.views.users import UserForm

class LoginForm(FlaskForm):
    login = StringField('Uživatelské jméno',validators=[InputRequired(message="Zadejte uživatelské jméno!")])
    password = PasswordField('Heslo', validators=[InputRequired(message="Zadejte heslo!")])
    remember_me = BooleanField('Pamatuj si mě')

class FirstLoginForm(UserForm):
    employee = None
    role = None

    def __init__(self,*args, **kwargs):
        super(FlaskForm,self).__init__(*args, **kwargs)


class FirstLogin(MethodView):
    def get(self,user_id):
        user = db.get_user_by_attr(id=user_id)
        return render_template('login_first.html', form=FirstLoginForm(obj=user), user_id=user.id)

    def post(self,user_id):
        form = FirstLoginForm(request.form)
        user = db.get_user_by_attr(id=user_id)
        if form.validate_on_submit():
            if not db.is_login_valid(form.data['login']):
                flash("Zvolte jiné uživatelské jméno, '%s' je již používáno!" % form.data['login'], 'alert alert-danger')
                return redirect(url_for('first-login', user_id=user.id))
            db.edit_user_from_form(user_id, form.data)
            login_user(user)
            db.log_visit(user)
            flash("Uživatelské jméno a heslo úspěšně změněno!", 'alert alert-success')
            return redirect(url_for('dashboard_empl')) if user.is_employee() else redirect(url_for('dashboard_boss'))
        return render_template('login_first.html', form=form, user_id=user_id)


def is_first_login(user):
    return True if user.poc_prihl is None else False


def configure_login(app):

    app.add_url_rule('/first_login/<int:user_id>', view_func=FirstLogin.as_view('first-login'))

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
                flash("Neznámé uživatelské jméno!", 'alert alert-danger')
            elif not user.check_password(form.password.data):
                flash("Neplatné heslo!", 'alert alert-danger')
            else:
                #TODO: Jestli se uzivatel prihlasuje poprve, musi si zmenit heslo
                if is_first_login(user):
                    flash("Toto je Vaše první přihlášení - změňte si uživatelské jméno a heslo!", 'alert alert-success')
                    return redirect(url_for('first-login', user_id=user.id))
                login_user(user, remember=form.remember_me.data)
                db.log_visit(user)
                flash("Přihlášení proběhlo úspěšně!", 'alert alert-success')
                if user.is_employee():
                    return redirect(url_for('dashboard_empl'))
                else:
                    return redirect(url_for('dashboard_boss'))
        return render_template('login.html', title='Přihlášení', form=form, error=error)
