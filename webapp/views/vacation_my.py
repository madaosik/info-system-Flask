from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user
from flask.views import MethodView
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import InputRequired
from webapp.roles import admin, employee, norestrict
from czech_holidays import Holidays

from webapp.core.models import *
from webapp.views.forms import CzechDateField

from webapp.core import db

import datetime


class VacationForm(FlaskForm):
    od = CzechDateField('Datum začátku', validators=[InputRequired(message="Doplňte datum začátku dovolené!")])
    do = CzechDateField('Datum konce (včetně)', validators=[InputRequired(message="Doplňte datum konce dovolené!")])
    submit = SubmitField('Uložit')

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        result = True
        if self.od.data > self.do.data:
            self.od.errors.append('Začátek dovolené musí mít dřívejší datum než její konec!')
            result = False
        return result


class MyVacation(MethodView):
    @norestrict
    def get(self):
        id_zam=request.args.get('id')
        instance = db.fetch_vacation_by_id(id_zam)
        return render_template('vacation_my.html', id=id_zam, me=instance, date=datetime.datetime.now().date())


class VacationAdd(MethodView):
    @norestrict
    def get(self):
        return render_template('vacation_form.html', form=VacationForm())

    def post(self):
        vacform = VacationForm()
        instance = db.get_obj_by_clsname(Dovolena_zam_hist)
        if not vacform.validate_on_submit():
            return render_template('vacation_form.html', form=vacform)
        id_zam = request.args.get('id_zam')
        requests = db.fetch_vacation_by_id(id_zam)
        db.update_from_form(instance, vacform)
        instance.id_zam = current_user.id_zam
        instance.celkem = (instance.do - instance.od).days + 1
        for one in requests:
            if (one.od <= instance.od <= one.do) or (one.od <= instance.do <= one.do) or (one.od > instance.od and one.do < instance.do ):
                flash("Evidujeme již Vaši žádost o dovolenou od %s do %s!" % (one.od.isoformat(), one.do.isoformat()), 'alert alert-danger')
                return render_template('vacation_form.html', form=vacform)
        if 6 <= instance.od.isoweekday():
            flash("Dovolená nesmí začínat během víkendových dní!",'alert alert-danger')
            return render_template('vacation_form.html', form=vacform)
        if 6 <= instance.do.isoweekday():
            flash("Dovolená nesmí končit během víkendových dní!", 'alert alert-danger')
            return render_template('vacation_form.html', form=vacform)
        if instance.od.year != instance.do.year:
            holidays_to = Holidays(instance.do.year)
            err = holiday_check(holidays_to, instance)
            if err != 0:
                return render_template('vacation_form.html', form=vacform)
            
        holidays = Holidays(instance.od.year)
        err = holiday_check(holidays, instance)
        if err == 'stateholidaystart':
            flash("Dovolená nesmí začínat v den státního svátku!!", 'alert alert-danger')
        elif err == 'stateholidayend':
            flash("Dovolená nesmí končit v den státního svátku!", 'alert alert-danger')
        if err:
            return render_template('vacation_form.html', form=vacform)

        if instance.od.isoweekday() > instance.do.isoweekday():
            instance.celkem -= 2
        db.add(instance)
        flash("Žádost o dovolenou byla úspěšně vytvořena a odeslána ke schválení!", 'alert alert-success')
        if instance.od < datetime.datetime.now().date():
            flash("Žádost o dovolenou byla vytvořena do minulosti!", 'alert alert-warning')
        return redirect(url_for('my_vacation', id=current_user.id_zam))


def holiday_check(holidays, instance):
    holidays.pop(0)  # because new year has a duplicity there
    for day in holidays:  # check for holidays
        if instance.do > day > instance.od and day.isoweekday() < 6:
            instance.celkem -= 1
        if day == instance.od:
            return 'stateholidaystart'
            error = "Dovolená nesmí začínat v den státního svátku!"
            return error
        elif day == instance.do:
            error = "Dovolená nesmí končit v den státního svátku!"
            return 'stateholidayend'
    return None


class VacationDelete(MethodView):
    @employee
    def post(self):
        id_zam = request.args.get('id')
        vacation = db.get_obj_by_id(Dovolena_zam_hist, request.args.get('id_vac'))
        db.delete(vacation)
        flash("Žádost o dovolenou byla úspěšně SMAZANA!", 'alert alert-success') #gramatika
        vac = db.fetch_vacation_by_id(id_zam)
        return render_template('vacation_my.html', id=id_zam, me=vac, date=datetime.datetime.now().date())


def configure(app):
    app.add_url_rule('/my_vacation', view_func=MyVacation.as_view('my_vacation'))
    app.add_url_rule('/vacations_add', view_func=VacationAdd.as_view('vacation-add'))
    app.add_url_rule('/my_vacation_del', view_func=VacationDelete.as_view('my_vacation_delete'))

