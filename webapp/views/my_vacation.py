from flask import render_template, redirect, url_for, request
from flask.views import MethodView
from webapp.core import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField, PasswordField, SelectField
from wtforms.validators import InputRequired, DataRequired
from wtforms.fields.html5 import DateField
from webapp.roles import admin,current_user,employee
from czech_holidays import Holidays


from webapp.core.models import *
from webapp.views.forms import *

from webapp.core import db

import datetime

class CzechDateField(DateField):
    """
    Overrides the process_formdata() method definition in a standard DateField
    """
    def process_formdata(self, valuelist):
        if valuelist:
            date_str = ' '.join(valuelist)
            try:
                self.data = datetime.datetime.strptime(date_str, self.format).date()
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Neplatný formát data!'))


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
    def get(self):
        id_zam=request.args.get('id')
        instance = db.fetch_vacation_by_id(id_zam)
        return render_template('vacation_my.html', id=id_zam, me=instance, date=datetime.datetime.now().date())


class VacationAdd(MethodView):
    @employee
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
                error = "Zadost o dovolene v danem case od " + one.od.isoformat() + " do " + one.do.isoformat() + " uz existuje!"  #prelozit
                return render_template('vacation_form.html', form=vacform, error=error)
        if 6 <= instance.od.isoweekday():
            error = "Dovolena se nesmi zacit pres vikend!"  # prelozit
            return render_template('vacation_form.html', form=vacform, error=error)
        if 6 <= instance.do.isoweekday():
            error = "Dovolena se nesmi koncit pres vikend!"  # prelozit
            return render_template('vacation_form.html', form=vacform, error=error)
        if instance.od.year != instance.do.year:
            holidays_to = Holidays(instance.do.year)
            err = holiday_check(holidays_to, instance)
            if err != 0:
                return render_template('vacation_form.html', form=vacform, error=err)
            
        holidays = Holidays(instance.od.year)
        err = holiday_check(holidays, instance)
        if err != 0:
            return render_template('vacation_form.html', form=vacform, error=err)

        if instance.od.isoweekday() > instance.do.isoweekday():
            instance.celkem -= 2
        db.add(instance)
        return redirect(url_for('my_vacation', id=current_user.id_zam))


def holiday_check(holidays, instance):
    holidays.pop(0)  # because new year has a duplicity there
    for day in holidays:  # check for holidays
        if instance.do > day > instance.od and day.isoweekday() < 6:
            instance.celkem -= 1
        if day == instance.od:
            error = "Dovolena se nesmi zacinat pres svatek!"  # prelozit
            return error
        elif day == instance.do:
            error = "Dovolena se nesmi koncit pres svatek!"  # prelozit
            return error
    return 0


def configure(app):
    app.add_url_rule('/my_vacation', view_func=MyVacation.as_view('my_vacation'))
    app.add_url_rule('/vacations_add', view_func=VacationAdd.as_view('vacation-add'))
