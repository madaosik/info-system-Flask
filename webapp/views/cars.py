from flask import render_template, request, redirect, flash
from flask.views import MethodView
from webapp.core import db
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import InputRequired, NumberRange

from webapp.core.models import Vozidlo
from webapp.roles import admin, management

class CarForm(FlaskForm):
    spz = StringField('* SPZ', validators=[InputRequired("Zadejte SPZ!")])
    znacka = StringField('* Značka', validators=[InputRequired("Zadejte značku vozidla!")])
    model = StringField('Model')
    rok_vyroby = IntegerField('* Rok výroby', validators=[NumberRange(min=1995,max=2018,message="Zadejte platný rok výroby!")])
    vykon = IntegerField('Výkon(kw)')
    nosnost = IntegerField('Nosnost')
    pocet_naprav = IntegerField('* Počet náprav', validators=[NumberRange(min=2,max=10,message="Zadejte počet náprav mezi 2 a 10!")])
    emisni_trida = StringField('Emisní třída')
    submit = SubmitField('Uložit')

class Cars(MethodView):
    @management
    def get(self):
        return render_template('cars.html', cars=db.fetch_all_cars())


class CarsAdd(MethodView):
    @management
    def get(self):
        return render_template('car_form.html', form=CarForm())

    @management
    def post(self):
        carform = CarForm()
        if not carform.validate_on_submit():
            return render_template('car_form.html', form=carform)
        car = Vozidlo()
        carform.populate_obj(car)
        db.add(car)
        flash("Vozidlo '%s' úspěšně přidáno!" % car.spz, 'alert alert-success')
        return redirect('cars')


class CarsDelete(MethodView):
    @management
    def get(self):
        db.delete_car(request.args.get('id'))
        return redirect('cars')


class CarsModify(MethodView):
    @management
    def get(self):
        car = db.fetch_car(request.args.get('id'))
        carform = CarForm(obj=car)
        return render_template('car_form.html', car=car, form=carform)

    @management
    def post(self):
        carform = CarForm(request.form)
        if not carform.validate_on_submit():
            return render_template('car_form.html', form=carform)
        car = db.fetch_car(request.form.get('id'))
        db.update_from_form(car, carform)
        flash("Vozidlo '%s' úspěšně upraveno!" % car.spz, 'alert alert-success')
        return redirect('cars')

class CarProfiles(MethodView):
    @management
    def get(self):
        return render_template('car_profiles.html', cars=db.fetch_all_cars())

class EditCarProfile(MethodView):
    @management
    def get(self):
        pass
        # employee = db.get_empl_from_user(current_user.id)
        # return render_template('my_profile_form.html', employee=employee, form=EditProfileForm(obj=employee), form_accessdata=EditAccessForm(obj=current_user))

    def post(self):
        pass
        # id_zam = request.form.get('id_zam')
        # editform = EditProfileForm()
        # employee = db.fetch_employee_by_id(id_zam)
        # if not editform.validate_on_submit():
        #     return render_template('my_profile_form.html', employee=employee, form=editform)
        # db.update_from_form(employee, editform)
        # flash('Úprava profilu proběhla úspěšně!', 'alert alert-success')
        # return redirect(url_for('employeeprofile', id_zam=id_zam))



def configure(app):
    app.add_url_rule('/cars', view_func=Cars.as_view('cars'))
    app.add_url_rule('/cars_add', view_func=CarsAdd.as_view('car-add'))
    app.add_url_rule('/cars_delete', view_func=CarsDelete.as_view('car-del'))
    app.add_url_rule('/cars_modify', view_func=CarsModify.as_view('car-mod'))
    app.add_url_rule('/car_profiles', view_func=CarProfiles.as_view('car-profiles'))
