from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user
from flask.views import MethodView
from webapp.core import db
from webapp.roles import management

from webapp.views.employees import EmployeeForm
from webapp.views.users import UserEditForm


class CarProfile(MethodView):
    @management
    def get(self):
        return render_template('car_profile.html', cars=db.fetch_all_cars())

class EditProfile(MethodView):
    @management
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
        return redirect(url_for('profile', id_zam=id_zam))

def configure(app):
    app.add_url_rule('/car_profile', view_func=CarProfile.as_view('car_profile'))


