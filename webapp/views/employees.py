from flask import render_template, request, redirect, flash
from flask.views import MethodView
from webapp.core import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Email

from webapp.core.models import Zamestnanec, Uzivatel
from webapp.roles import admin
from webapp.views.forms import CzechDateField

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

class Employees(MethodView):
    @admin
    def get(self):
        return render_template('employees.html', empls=db.fetch_all_by_cls(Zamestnanec))


class EmployeeAdd(MethodView):
    @admin
    def get(self):
        return render_template('employee_form.html', form=EmployeeForm())

    @admin
    def post(self):
        employeeform = EmployeeForm()
        if not employeeform.validate_on_submit():
            #flash('Zadali jste neplatné údaje', 'alert-danger')
            error = "Zadali jste neplatné údaje"
            return render_template('employee_form.html', form=employeeform, error=error)
        employee = Zamestnanec()
        employeeform.populate_obj(employee)
        id = db.add_employee(employee)
        login = db.user_create(id,employee.prijmeni)
        if id:
            flash("Zaměstnanec %s %s úspěšně přidán!" % (employee.kr_jmeno, employee.prijmeni))
        else:
            flash("Zaměstnanec se jménem %s %s se nepodařilo přidat!" % (employee.kr_jmeno, employee.prijmeni), 'alert-error')
        if login:
            flash("Uživatel s loginem %s úspěšně přidán!" % login)
        else:
            flash("Nepodařilo se vytvořit uživatele!", 'alert-error')
        return redirect('employees')


class EmployeeDelete(MethodView):
    @admin
    def get(self):
        db.delete_employee(request.args.get('id'))
        flash("Zaměstnanec úspěšně smazán!")
        return redirect('employees')


class EmployeeModify(MethodView):
    @admin
    def get(self):
        employee = db.fetch_employee_by_id(request.args.get('id'))
        emplform = EmployeeForm(obj=employee)
        return render_template('employee_form.html', employee=employee, form=emplform)

    @admin
    def post(self):
        emplform = EmployeeForm(request.form)
        if not emplform.validate_on_submit():
            #flash('Zadali jste neplatné údaje', 'alert-danger')
            error = "Zadali jste neplatné údaje"
            return render_template('employee_form.html', form=emplform, error=error)
        employee = db.fetch_employee_by_id(request.form.get('id'))
        db.update_from_form(employee, emplform)
        flash("Úprava zaměstnance %s %s byla úspěšná!" % (employee.kr_jmeno, employee.prijmeni))
        return redirect('employees')


def configure(app):
    app.add_url_rule('/employees', view_func=Employees.as_view('employees'))
    app.add_url_rule('/employees_add', view_func=EmployeeAdd.as_view('employee-add'))
    app.add_url_rule('/employees_delete', view_func=EmployeeDelete.as_view('employee-del'))
    app.add_url_rule('/employees_modify', view_func=EmployeeModify.as_view('employee-mod'))