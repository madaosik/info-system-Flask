from flask import render_template, request, redirect,url_for
from flask.views import MethodView
from webapp.core import db
from webapp.roles import employee
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Email


class EditMeForm(FlaskForm):
    trv_bydliste = StringField('Trvalé bydliště')
    prech_bydliste = StringField('Přechodné bydliště')
    telefon = StringField('Telefon')
    email = StringField('* E-mail', validators=[Email(message="E-mailová adresa nemá správný formát!")])
    submit = SubmitField('Uložit')


class Profile(MethodView):
    @employee
    def get(self):
        id_zam = request.args.get('id_zam')
        instance = db.fetch_employee_by_id(id_zam)
        print(id_zam)
        return render_template('profile.html', me=instance)


class EditMe(MethodView):
    @employee
    def get(self):
        instance = db.fetch_employee_by_id(request.args.get('id_zam'))
        editform = db.get_obj_by_clsname(EditMeForm, initobject=instance)
        return render_template('employee_edit_form.html', employee=instance, form=editform, action='edit_me')

    def post(self):
        id_zam = request.form.get('id_zam')
        edit_form = EditMeForm()
        print(id_zam)
        instance = db.fetch_employee_by_id(id_zam)
        if edit_form.validate_on_submit():
            db.update_from_form(instance, edit_form)
            return redirect(url_for('profile', id_zam=id_zam))
        return render_template('employee_edit_form.html', employee=instance, form=EditMeForm(), action='edit_me')


def configure(app):
    app.add_url_rule('/profile', view_func=Profile.as_view('profile'))
    app.add_url_rule('/profile_edit', view_func=EditMe.as_view('edit_me'))

