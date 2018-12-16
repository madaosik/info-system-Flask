from flask import render_template, request, redirect, flash, url_for
from flask.views import MethodView
from webapp.core import db
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import InputRequired, NumberRange

from webapp.core.models import Vozidlo
from webapp.roles import admin, management
from webapp.views.forms import CzechDateField

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

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        result = True
        if not 9 > len(self.spz.data) >= 7:
            self.spz.errors.append('Zadejte validní ŠPZ!')
            result = False
        return result

class CarDeadlineEditForm(FlaskForm):
    date_expiry = CzechDateField('Nový termín', validators=[InputRequired(message="Doplňte nový termín!")])
    submit = SubmitField('Uložit')


class CarServiceDiarySelector(FlaskForm):
    cars = SelectField('Servisni deník pro vozidlo:')

    def __init__(self,*args,**kwargs):
        super(CarServiceDiarySelector,self).__init__(*args, **kwargs)
        self.cars.choices = db.get_cars_tuples()

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


# VARIOUS CAR CONSTANTS


class CarProfiles(MethodView):
    car_deadline_types = {'techprobe': 1, 'tachoprobe': 2, 'fireprobe': 3}

    @management
    def get(self):
        car_profiles = db.get_car_profile_data(self.car_deadline_types)
        edit_form = CarDeadlineEditForm()
        return render_template('car_profiles.html', car_profiles=car_profiles, form=edit_form)

class CarDeadlineAdd(CarProfiles):
    deadline_type_str = {'techprobe': 'technické prohlídky', 'tachoprobe': 'prohlídky tachografu', 'fireprobe': 'prohlídky hasícího přístroje'}

    @management
    def post(self):
        form = CarDeadlineEditForm()
        print(request.form.get('car_id'))
        db.car_deadline_add(request.form.get('car_id'), request.form.get('deadline_type'), form.date_expiry.data, self.car_deadline_types)
        flash("Datum expirace %s u vozidla '%s' bylo úspěšně stanoveno na %s!" % (self.deadline_type_str[request.form.get('deadline_type')], request.form.get('car_spz'), form.date_expiry.data.strftime("%d. %m. %Y")), 'alert alert-success')
        return redirect(url_for('car-profiles'))

class CarDeadlineEdit(CarDeadlineAdd):

    @management
    def post(self):
        form = CarDeadlineEditForm()
        deadline_id = request.form.get('id_deadline')
        db.car_deadline_edit(deadline_id, form.date_expiry.data)
        flash("Datum expirace %s u vozidla '%s' bylo úspěšně změněno na %s!" % (self.deadline_type_str[request.form.get('deadline_type')], request.form.get('car_spz'), form.date_expiry.data.strftime("%d. %m. %Y")), 'alert alert-success')
        return redirect(url_for('car-profiles'))

class CarServiceDiary(MethodView):
    @management
    def get(self):
        car_id = db.get_first_car_id()
        return render_template('car_servicediary.html',selector=CarServiceDiarySelector(),service_history=db.fetch_service_history(car_id))

def configure(app):
    app.add_url_rule('/cars', view_func=Cars.as_view('cars'))
    app.add_url_rule('/cars_add', view_func=CarsAdd.as_view('car-add'))
    app.add_url_rule('/cars_delete', view_func=CarsDelete.as_view('car-del'))
    app.add_url_rule('/cars_modify', view_func=CarsModify.as_view('car-mod'))
    app.add_url_rule('/car_profiles', view_func=CarProfiles.as_view('car-profiles'))
    app.add_url_rule('/car_deadline_edit', view_func=CarDeadlineEdit.as_view('car-deadline-edit'))
    app.add_url_rule('/car_deadline_add', view_func=CarDeadlineAdd.as_view('car-deadline-add'))
    app.add_url_rule('/car_service', view_func=CarServiceDiary.as_view('car-servicediary'))
