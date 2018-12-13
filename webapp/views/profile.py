from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user
from flask.views import MethodView
from webapp.core import db
from webapp.roles import employee

from webapp.views.employees import EmployeeForm

class EditProfileForm(EmployeeForm):
    kr_jmeno = None
    prijmeni = None
    dat_nar = None
    prac_sml = None
    aktivni = None

class Profile(MethodView):
    @employee
    def get(self):
        return render_template('my_profile.html', me=db.get_empl_from_user(current_user.id))


class EditProfile(MethodView):
    @employee
    def get(self):
        employee = db.get_empl_from_user(current_user.id)
        return render_template('my_profile_form.html', employee=employee, form=EditProfileForm(obj=employee))

    def post(self):
        id_zam = request.form.get('id_zam')
        editform = EditProfileForm()
        employee = db.fetch_employee_by_id(id_zam)
        if not editform.validate_on_submit():
            return render_template('my_profile_form.html', employee=employee, form=editform)
        db.update_from_form(employee, editform)
        flash('Úprava profilu proběhla úspěšně!', 'alert alert-success')
        return redirect(url_for('profile', id_zam=id_zam))


def configure(app):
    app.add_url_rule('/profile', view_func=Profile.as_view('profile'))
    app.add_url_rule('/profile_edit', view_func=EditProfile.as_view('profile-mod'))

