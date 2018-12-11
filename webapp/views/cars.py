from flask import render_template, request, redirect, flash
from flask.views import MethodView
from webapp.core import db
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import InputRequired, NumberRange

from webapp.core.models import Vozidlo
from webapp.roles import admin

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
    @admin
    def get(self):
        return render_template('cars.html', cars=db.fetch_all_cars())


class CarsAdd(MethodView):
    @admin
    def get(self):
        return render_template('car_form.html', form=CarForm())

    @admin
    def post(self):
        carform = CarForm()
        if not carform.validate_on_submit():
            #flash('Zadali jste neplatné údaje', 'alert-danger')
            error = "Zadali jste neplatné údaje"
            return render_template('car_form.html', form=carform, error=error)
        car = Vozidlo()
        carform.populate_obj(car)
        db.add(car)
        flash("Vozidlo úspěšně přidáno!")
        return redirect('cars')


class CarsDelete(MethodView):
    @admin
    def get(self):
        db.delete_car(request.args.get('id'))
        return redirect('cars')


class CarsModify(MethodView):
    @admin
    def get(self):
        car = db.fetch_car(request.args.get('id'))
        carform = CarForm(obj=car)
        return render_template('car_form.html', car=car, form=carform)

    @admin
    def post(self):
        carform = CarForm(request.form)
        if not carform.validate_on_submit():
            #flash('Zadali jste neplatné údaje', 'alert-danger')
            error = "Zadali jste neplatné údaje"
            return render_template('car_form.html', form=carform, error=error)
        car = db.fetch_car(request.form.get('id'))
        db.update_from_form(car, carform)
        return redirect('cars')


def configure(app):
    app.add_url_rule('/cars', view_func=Cars.as_view('cars'))
    app.add_url_rule('/cars_add', view_func=CarsAdd.as_view('car-add'))
    app.add_url_rule('/cars_delete', view_func=CarsDelete.as_view('car-del'))
    app.add_url_rule('/cars_modify', view_func=CarsModify.as_view('car-mod'))