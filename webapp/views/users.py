from flask import render_template, request, redirect, flash, url_for
from flask.views import MethodView
from webapp.core import db
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, PasswordField, StringField
from wtforms.validators import EqualTo, DataRequired

from webapp.core.models import Uzivatel
from webapp.roles import admin, get_role_tuples, get_role_dict

class UserForm(FlaskForm):
    employee = SelectField('Přiřazený zaměstnanec', coerce=int)
    role = SelectField('Role')
    login = StringField('Uživatelské jméno', validators=[DataRequired(message="Zadejte uživatelské jméno")])
    password = PasswordField('Heslo', validators=[DataRequired(message="Zadejte heslo!")])
    password2 = PasswordField('Zopakování hesla', validators=[DataRequired(), EqualTo('password',message="Zadaná hesla se neshodují!")])
    submit = SubmitField('Uložit')

    def fill_role_selectbox(self, roles):
        self.role.choices = roles

    def fill_employee_selectbox(self, employees):
        self.employee.choices = employees

class UserEditForm(UserForm):
    # Heslo při editaci nechceme jako povinné pole a login nejde měnit.....
    employee = None
    password = PasswordField('Heslo')
    password2 = PasswordField('Zopakování hesla',validators=[EqualTo('password', message="Zadaná hesla se neshodují!")])
    submit = SubmitField('Uložit')

class Users(MethodView):
    @admin
    def get(self):
        users_empls = db.fetch_user_tuples()
        return render_template('users.html', users=users_empls, role_dict=get_role_dict())


class UserAdd(MethodView):
    @admin
    def get(self):
        userform = UserForm()
        userform.fill_role_selectbox(get_role_tuples())
        userform.fill_employee_selectbox(db.get_employee_tuples())
        if not userform.employee.choices:
            flash('Všichni zaměstnanci mají aktuálně přiřazeného uživatele, operaci tudíž nelze provést!', 'alert alert-danger')
            return redirect(url_for('users'))
        return render_template('user_form.html', form=userform)

    @admin
    def post(self):
        userform = UserForm(request.form)
        userform.fill_role_selectbox(get_role_tuples())
        userform.fill_employee_selectbox(db.get_employee_tuples())
        if not userform.validate_on_submit():
            return render_template('user_form.html', form=userform)
        user = Uzivatel()
        userform.populate_obj(user)
        if db.is_login_valid(user.login):
            login = db.create_user(login=user.login, password=user.password, employee_id=userform.employee.data)
            flash("Uživatel '%s' byl úspěšně přidán!" % login, 'alert alert-success')
            return redirect('users')
        else:
            flash("Uživatel se jménem '%s' již existuje!" % user.login, 'alert alert-danger')
            return render_template('user_form.html', form=userform)


class UserDelete(MethodView):
    @admin
    def get(self):
        db.delete_user(request.args.get('id'))
        flash("Uživatel úspěšně smazán!", 'alert alert-success')
        return redirect('users')


class UserModify(MethodView):
    @admin
    def get(self):
        user = db.get_user_by_attr(id=request.args.get('id'))
        employee = db.fetch_employee_by_id(user.id_zam)
        userform = UserEditForm(obj=user)
        userform.fill_role_selectbox(get_role_tuples())
        return render_template('user_form.html', user=user, employee=employee, form=userform)

    @admin
    def post(self):
        userform = UserEditForm(request.form)
        userform.fill_role_selectbox(get_role_tuples())
        if not userform.validate_on_submit():
            flash('Zadali jste neplatné údaje', 'alert alert-danger')
            return render_template('user_form.html', form=userform)
        user = db.get_user_by_attr(id=request.form.get('id'))
        db.edit_user_from_form(user.id, userform.data)
        flash("Úprava uživatele '%s' byla úspěšná!" % user.login, 'alert alert-success')
        return redirect('users')


def configure(app):
    app.add_url_rule('/users', view_func=Users.as_view('users'))
    app.add_url_rule('/users_add', view_func=UserAdd.as_view('user-add'))
    app.add_url_rule('/users_delete', view_func=UserDelete.as_view('user-del'))
    app.add_url_rule('/users_modify', view_func=UserModify.as_view('user-mod'))