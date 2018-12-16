from flask import render_template, redirect, url_for, request, flash
from flask.views import MethodView
import datetime
from flask_login import current_user

from webapp.roles import admin, management,employee, norestrict
from webapp.core.models import *
from webapp.core import db

from webapp.views.forms import CzechDateField
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import InputRequired
from czech_holidays import Holidays


class VacationEmployeeSelector(FlaskForm):
    empl = SelectField('Dovolená pro zaměstnance:')

    def __init__(self,*args,**kwargs):
        super(VacationEmployeeSelector,self).__init__(*args, **kwargs)
        self.empl.choices = db.get_employee_tuples()


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


class Vacations(MethodView):
    @management
    def get(self):
        all_instances = db.fetch_all_by_cls(Dovolena_zam_hist)
        empl = db.fetch_all_by_cls(Zamestnanec)
        return render_template('vacations.html', all=all_instances, empl=empl, date=datetime.datetime.now().date())


class VacationsHist(MethodView):
    @management
    def get(self):
        a = VacationEmployeeSelector()
        vac = db.fetch_all_by_cls(Dovolena_zam_hist)
        return render_template('vacation_hist.html', vac=vac, selector=VacationEmployeeSelector(), id=a.empl.data,
                               date=datetime.datetime.now().date())

    def post(self):
        a = VacationEmployeeSelector()
        vac = db.fetch_vacation_by_id(a.empl.data)
        return render_template('vacation_hist.html', selector=VacationEmployeeSelector(), id=a.empl.data, me=vac,
                               date=datetime.datetime.now().date())


class VacationsHistOne(MethodView):
    @management
    def get(self):
        id_zam = request.args.get('id')
        instance = db.fetch_vacation_by_id(id_zam)
        empl = db.fetch_all_by_cls(Zamestnanec)
        check = db.fetch_vacation_by_id(id_zam).first()
        return render_template('vacation_hist_detail.html', empl=empl, me=instance, date=datetime.datetime.now().date(),check=check)


class VacationApprove(MethodView):
    @management
    def post(self):
        db.approve(Dovolena_zam_hist, request.args.get('id'))  #instance = db.get_obj_by_id(Dovolena_zam_hist, id)
        flash("Žádost o dovolenou byla úspěšně SCHVÁLENA!", 'alert alert-success')
        return redirect(url_for('vacations'))


class VacationDecline(MethodView):
    @management  # doplnit
    def post(self):
        instance = db.get_obj_by_id(Dovolena_zam_hist, request.args.get('id'))
        db.delete(instance)
        flash("Žádost o dovolenou byla úspěšně ZAMÍTNUTA!", 'alert alert-success')
        return redirect(url_for('vacations'))


class MyVacation(MethodView):
    @norestrict
    def get(self):
        id_zam=request.args.get('id')
        if id_zam is None:
            id_zam=current_user.id_zam
        vacations = db.fetch_vacation_by_id(id_zam)
        if current_user.id_zam == id_zam:
            db.mark_seen_zam_vacation(id_zam)
        return render_template('vacation_my.html', id=id_zam, me=vacations, date=datetime.datetime.now().date())


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
            if err == 'stateholidaystart':
                flash("Dovolená nesmí začínat v den státního svátku!!", 'alert alert-danger')
            elif err == 'stateholidayend':
                flash("Dovolená nesmí končit v den státního svátku!", 'alert alert-danger')
            if err:
                return render_template('vacation_form.html', form=vacform)
        holidays = Holidays(instance.od.year)
        err = holiday_check(holidays, instance)
        if err == 'stateholidaystart':
            flash("Dovolená nesmí začínat v den státního svátku!!", 'alert alert-danger')
        elif err == 'stateholidayend':
            flash("Dovolená nesmí končit v den státního svátku!", 'alert alert-danger')
        if err:
            return render_template('vacation_form.html', form=vacform)

        if instance.od.isoweekday() >= instance.do.isoweekday() and instance.od != instance.do:
            instance.celkem -= 2
        if (instance.do - instance.od).days > 7:
            for x in range(0, (instance.do - instance.od).days//7):
                instance.celkem -= 2
        instance.rok = instance.od.year
        db.add(instance)
        flash("Žádost o dovolenou byla úspěšně vytvořena a odeslána ke schválení!", 'alert alert-success')
        if instance.od < datetime.datetime.now().date():
            flash("Žádost o dovolenou byla vytvořena do minulosti!", 'alert alert-warning')
        return redirect(url_for('my_vacation', id=current_user.id_zam))


def holiday_check(holidays, instance):
    holidays.pop(0)  # because new year has a duplicity there
    for day in holidays:  # check for holidays
        error = None
        if instance.do > day > instance.od and day.isoweekday() < 6:
            instance.celkem -= 1
        if day == instance.od:
            error = "Dovolená nesmí začínat v den státního svátku!"
            return 'stateholidaystart'
        elif day == instance.do:
            error = "Dovolená nesmí končit v den státního svátku!"
            return 'stateholidayend'
    return error


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
    app.add_url_rule('/vacations', view_func=Vacations.as_view('vacations'))
    app.add_url_rule('/vacations_decline', view_func=VacationDecline.as_view('vac_decline'))
    app.add_url_rule('/vacations_approve', view_func=VacationApprove.as_view('vac_approve'))
    app.add_url_rule('/vacations_history', view_func=VacationsHist.as_view('vacations_hist'))
    app.add_url_rule('/vacations_history_one', view_func=VacationsHistOne.as_view('vacations_hist_one'))

    app.add_url_rule('/my_vacation', view_func=MyVacation.as_view('my_vacation'))
    app.add_url_rule('/vacations_add', view_func=VacationAdd.as_view('vacation-add'))
    app.add_url_rule('/my_vacation_del', view_func=VacationDelete.as_view('my_vacation_delete'))


