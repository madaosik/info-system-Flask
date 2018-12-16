from flask import render_template, request, redirect, flash, url_for
from flask_login import current_user
from flask.views import MethodView
from webapp.core import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Email

from webapp.core.models import Zamestnanec
from webapp.roles import management,employee
from webapp.views.forms import CzechDateField
from webapp.views.users import UserEditForm
import re

class EmployeeForm(FlaskForm):
    kr_jmeno = StringField('* Křestní jméno', validators=[InputRequired(message="Doplňte křestní jméno!")])
    prijmeni = StringField('* Příjmení', validators=[InputRequired(message="Doplňte příjmení!")])
    dat_nar = CzechDateField('Datum narození')
    trv_bydliste = StringField('Trvalé bydliště')
    prech_bydliste = StringField('Přechodné bydliště')
    telefon = StringField('Telefon')
    email = StringField('* E-mail', validators=[Email(message="E-mailová adresa nemá správný formát!")])
    prac_sml = StringField('Číslo pracovní sml.')
    aktivni = BooleanField('Aktivní', default='checked')
    submit = SubmitField('Uložit')

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        result = True

        if not telephone_is(self.telefon.data):
            self.telefon.errors.append('Zadejte validní číslo bez mezer!')
            result = False
        if 9 > len(self.telefon.data) or len(self.telefon.data) > 13:
            self.telefon.errors.append('Zadejte validní číslo bez mezer!')
            result = False
        if len(self.telefon.data) == 0:
            result = True

        return result


def telephone_is(string):
    tel = re.compile(r'[^+ 0-9]')
    num = re.compile(r'[^ 0-9]')
    a = string
    string = tel.search(string)
    a = num.search(a[1:])
    return not (bool(string) or bool(a))

class EditProfileForm(EmployeeForm):
    kr_jmeno = None
    prijmeni = None
    dat_nar = None
    prac_sml = None
    aktivni = None

class EditAccessForm(UserEditForm):
    role = None

class Employees(MethodView):
    @management
    def get(self):
        return render_template('employees.html', empls=db.fetch_all_by_cls(Zamestnanec))


class EmployeeAdd(MethodView):
    @management
    def get(self):
        return render_template('employee_form.html', form=EmployeeForm())

    @management
    def post(self):
        employeeform = EmployeeForm()
        if not employeeform.validate_on_submit():
            flash('Zadali jste neplatné údaje', 'alert alert-danger')
            return render_template('employee_form.html', form=employeeform)
        employee = Zamestnanec()
        employeeform.populate_obj(employee)
        id = db.add_employee(employee)
        login = db.create_user(employee_id=id)
        if id:
            flash("Zaměstnanec %s %s úspěšně přidán!" % (employee.kr_jmeno, employee.prijmeni), 'alert alert-success')
        else:
            flash("Zaměstnanec se jménem %s %s se nepodařilo přidat!" % (employee.kr_jmeno, employee.prijmeni), 'alert alert-danger')
        if login:
            flash("Uživatel s loginem %s úspěšně přidán!" % login, 'alert alert-success')
        else:
            flash("Nepodařilo se vytvořit uživatele!", 'alert alert-danger')
        return redirect('employees')


class EmployeeDelete(MethodView):
    @management
    def get(self):
        db.delete_employee(request.args.get('id'))
        flash("Zaměstnanec úspěšně smazán!",'alert alert-success')
        return redirect('employees')


class EmployeeModify(MethodView):
    @management
    def get(self):
        employee = db.fetch_employee_by_id(request.args.get('id'))
        emplform = EmployeeForm(obj=employee)
        return render_template('employee_form.html', employee=employee, form=emplform)

    @management
    def post(self):
        emplform = EmployeeForm(request.form)
        if not emplform.validate_on_submit():
            return render_template('employee_form.html', form=emplform)
        employee = db.fetch_employee_by_id(request.form.get('id'))
        db.update_from_form(employee, emplform)
        flash("Úprava zaměstnance %s %s byla úspěšná!" % (employee.kr_jmeno, employee.prijmeni),'alert alert-success')
        return redirect('employees')


class EmployeeProfile(MethodView):
    @employee
    def get(self):
        return render_template('my_profile.html', me=db.get_empl_from_user(current_user.id))

class EditEmployeeProfile(MethodView):
    @employee
    def get(self):
        employee = db.get_empl_from_user(current_user.id)
        return render_template('my_profile_form.html', employee=employee, form=EditProfileForm(obj=employee), form_accessdata=EditAccessForm(obj=current_user))

    def post(self):
        id_zam = request.form.get('id_zam')
        editform = EditProfileForm()
        employee = db.fetch_employee_by_id(id_zam)
        if not editform.validate_on_submit():
            return render_template('my_profile_form.html', employee=employee, form=editform)
        db.update_from_form(employee, editform)
        flash('Úprava profilu proběhla úspěšně!', 'alert alert-success')
        return redirect(url_for('employeeprofile', id_zam=id_zam))

class EditEmployeeAccess(MethodView):
    @employee
    def post(self):
        accessform = EditAccessForm(request.form)
        if not accessform.validate_on_submit():
            return redirect(url_for('employeeprofile-mod'))
        db.edit_user_from_form(current_user.id,accessform.data)
        flash('Úprava přistupových údajů proběhla úspěšně!', 'alert alert-success')
        return redirect(url_for('employeeprofile-mod'))


def configure(app):
    app.add_url_rule('/employees', view_func=Employees.as_view('employees'))
    app.add_url_rule('/employees_add', view_func=EmployeeAdd.as_view('employee-add'))
    app.add_url_rule('/employees_delete', view_func=EmployeeDelete.as_view('employee-del'))
    app.add_url_rule('/employees_modify', view_func=EmployeeModify.as_view('employee-mod'))
    app.add_url_rule('/profile', view_func=EmployeeProfile.as_view('employeeprofile'))
    app.add_url_rule('/profile_edit', view_func=EditEmployeeProfile.as_view('employeeprofile-mod'))
    app.add_url_rule('/profile_access_mod', view_func=EditEmployeeAccess.as_view('employeeprofile-access-mod'))