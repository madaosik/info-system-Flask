from flask import render_template, request, redirect, flash, url_for
from flask.views import MethodView
from webapp.core import db
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, TextAreaField
from wtforms.validators import InputRequired, NumberRange
from datetime import datetime, timedelta

from webapp.core.models import Vozidlo, ServiceHistory
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

class CarServiceForm(FlaskForm):
    car = SelectField('Vozidlo')
    short_desc = StringField('Úkon', validators=[InputRequired("Zadejte servisní úkon!")])
    long_desc = TextAreaField('Detailní popis')
    mileage = IntegerField('Stav tachometru (km)')
    mechanic = StringField('Provedl')
    receipt_no = StringField('Číslo dokladu')
    date = CzechDateField('Datum')
    submit = SubmitField('Uložit')

    def __init__(self,*args,**kwargs):
        super(CarServiceForm,self).__init__(*args, **kwargs)
        self.car.choices = db.get_cars_tuples()

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
        return redirect(url_for('car-profiles'))


class CarsDelete(MethodView):
    @management
    def get(self):
        car = db.fetch_car(request.args.get('id'))
        spz = car.spz
        db.delete_car(request.args.get('id'))
        flash("Vozidlo '%s' úspěšně smazáno!" % spz, 'alert alert-success')
        return redirect(url_for('cars'))


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
        return redirect(url_for('car-profiles'))


class CarProfiles(MethodView):
    car_deadline_types = {'techprobe': 1, 'tachoprobe': 2, 'fireprobe': 3}

    @management
    def get(self):
        car_profiles = db.get_car_profile_data(self.car_deadline_types)
        edit_form = CarDeadlineEditForm()
        today = datetime.now().date()
        return render_template('car_profiles.html', car_profiles=car_profiles, form=edit_form, today=today, upcoming_tresh=today + timedelta(days=15), overdue_tresh = today + timedelta(days=7))

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


class CarDeadlineDelete(CarDeadlineAdd):
    @management
    def post(self):
        deadline_id = request.form.get('dl_id')
        db.car_deadline_delete(deadline_id)
        flash("Datum expirace %s u vozidla '%s' bylo úspěšně odstraněno!" % (self.deadline_type_str[request.form.get('deadline_type')],request.form.get('car_spz')), 'alert alert-success')
        return redirect(url_for('car-profiles'))


class CarServiceDiary(MethodView):
    @management
    def get(self,car_id):
        if car_id == 0:
            shown_car_id = db.get_first_car_id()
        else:
            shown_car_id = car_id
        car = db.fetch_car(shown_car_id)
        return render_template('car_servicediary.html',selector=CarServiceDiarySelector(cars=shown_car_id),service_history=db.fetch_service_history(shown_car_id),car=car)


class CarServiceDiaryChange(MethodView):
    @management
    def post(self):
        car_id = request.form.get('cars')
        car = db.fetch_car(car_id)
        return redirect(url_for('car-service-diary',car_id=car_id))

class CarServiceAdd(MethodView):

    @management
    def get(self):
        form = CarServiceForm(car=car_id)
        return render_template('car_service_add.html',form=form,car_id=car_id)

    @management
    def post(self):
        form = CarServiceForm(obj=request.form)
        car_id = request.form.get('car_id')
        db.service_add(request.form)
        return redirect(url_for('car-service-diary',car_id=car_id))

class CarServiceModify(MethodView):
    pass

class CarServiceDelete(MethodView):
    pass

def configure(app):
    app.add_url_rule('/cars', view_func=Cars.as_view('cars'))
    app.add_url_rule('/cars_add', view_func=CarsAdd.as_view('car-add'))
    app.add_url_rule('/cars_delete', view_func=CarsDelete.as_view('car-del'))
    app.add_url_rule('/cars_modify', view_func=CarsModify.as_view('car-mod'))
    app.add_url_rule('/car_profiles', view_func=CarProfiles.as_view('car-profiles'))
    app.add_url_rule('/car_deadline_edit', view_func=CarDeadlineEdit.as_view('car-deadline-edit'))
    app.add_url_rule('/car_deadline_add', view_func=CarDeadlineAdd.as_view('car-deadline-add'))
    app.add_url_rule('/car_deadline_del', view_func=CarDeadlineDelete.as_view('car-deadline-del'))
    app.add_url_rule('/car_service/<int:car_id>', view_func=CarServiceDiary.as_view('car-service-diary'))
    app.add_url_rule('/car_service_change', view_func=CarServiceDiaryChange.as_view('car-service-diary-change'))
    app.add_url_rule('/car_service_add', view_func=CarServiceAdd.as_view('car-service-add'))
    app.add_url_rule('/car_service_mod', view_func=CarServiceModify.as_view('car-service-mod'))
    app.add_url_rule('/car_service_del', view_func=CarServiceDelete.as_view('car-service-del'))

