from flask import render_template, request, redirect, flash
from flask.views import MethodView
from webapp.core import db
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, PasswordField, StringField
from wtforms.validators import EqualTo, DataRequired

from webapp.core.models import Uzivatel
from webapp.roles import admin

class UserForm(FlaskForm):
    login = StringField('Uživatelské jméno', validators=[DataRequired(message="Zadejte uživatelské jméno")])
    password = PasswordField('Heslo', validators=[DataRequired(message="Zadejte heslo!")])
    password2 = PasswordField('Zopakování hesla', validators=[DataRequired(), EqualTo('password',message="Zadaná hesla se neshodují!")])
    employee = SelectField('Zaměstnanec')
    role = SelectField('Role')
    submit = SubmitField('Uložit')

    def __init__(self,roles,employees, *args, **kwargs):
        super(UserForm,self).__init__(*args, **kwargs)
        self.fill_role_selectbox(roles)
        self.fill_employee_selectbox(employees)

    def fill_role_selectbox(self, roles):
        self.role.choices = roles

    def fill_employee_selectbox(self, employees):
        self.employee.choices = employees

class UserEditForm(UserForm):
    # Heslo při editaci nechceme jako povinné pole a login nejde měnit.....
    login = None
    role = SelectField('Role')
    password = PasswordField('Heslo')
    password2 = PasswordField('Zopakování hesla',validators=[EqualTo('password', message="Zadaná hesla se neshodují!")])
    submit = SubmitField('Uložit')

class Users(MethodView):
    @admin
    def get(self):
        users_empls = db.fetch_user_tuples()
        return render_template('users.html', users=users_empls)


class UserAdd(MethodView):
    @admin
    def get(self):
        return render_template('user_form.html', form=UserForm(db.get_role_tuples(),db.get_employee_tuples()))

    @admin
    def post(self):
        userform = UserForm(db.get_role_tuples(),db.get_employee_tuples())
        if not userform.validate_on_submit():
            flash('Zadali jste neplatné údaje', 'alert-danger')
            return render_template('employee_form.html', form=userform)
        user = Uzivatel()
        userform.populate_obj(user)
        # TODO: Zkontrolovat, jestli vybrany zamestnanec nema uz prirazeneho uzivatele
        db.add(employee)
        flash("Zaměstnanec se jménem %s %s úspěšně přidán!" % (employee.kr_jmeno, employee.prijmeni), 'alert-success')
        return redirect('employees')


class UserDelete(MethodView):
    @admin
    def get(self):
        db.delete_employee(request.args.get('id'))
        flash("Zaměstnanec úspěšně smazán!")
        return redirect('employees')


class UserModify(MethodView):
    @admin
    def get(self):
        user = db.get_user_by_attr(id=request.args.get('id'))
        userform = UserEditForm(db.get_role_tuples(),db.get_employee_tuples(),obj=user)
        return render_template('user_form.html', user=user, form=userform)

    @admin
    def post(self):
        emplform = UserEditForm(request.form)
        if not emplform.validate_on_submit():
            #flash('Zadali jste neplatné údaje', 'alert-danger')
            error = "Zadali jste neplatné údaje"
            return render_template('employee_form.html', form=emplform, error=error)
        employee = db.fetch_employee_by_id(request.form.get('id'))
        db.update_from_form(employee, emplform)
        flash("Úprava zaměstnance %s %s byla úspěšná!" % (employee.kr_jmeno, employee.prijmeni))
        return redirect('employees')


def configure(app):
    app.add_url_rule('/users', view_func=Users.as_view('users'))
    app.add_url_rule('/users_add', view_func=UserAdd.as_view('user-add'))
    app.add_url_rule('/users_delete', view_func=UserDelete.as_view('user-del'))
    app.add_url_rule('/users_modify', view_func=UserModify.as_view('user-mod'))