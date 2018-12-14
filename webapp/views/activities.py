from flask import render_template,request,redirect,url_for,flash
from flask_login import current_user
from flask.views import MethodView
from webapp.core import db
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField
from wtforms.validators import InputRequired
import datetime
from webapp.roles import employee, admin, management, norestrict
from webapp.core.models import *
from wtforms.fields.html5 import DateField, DateTimeField, DateTimeLocalField


class NewActivityForm(FlaskForm):
    type = StringField('Typ', default="Transport")
    vozidlo = SelectField('Vozidlo', coerce=int)
    from_place = StringField('Odkud', default="Brno-Tuřany")
    via_place = StringField('Přes')
    to_place = StringField('Kam', default="Brno-Tuřany")

    begin = DateTimeLocalField('Datum a čas odjezdu', default=datetime.datetime.now, format="%Y-%m-%dT%H:%M",
                              validators=[InputRequired(message="Doplňte den začátku aktivity!")])
    end = DateTimeLocalField('Datum a čas návratu', default=datetime.datetime.now, format="%Y-%m-%dT%H:%M",
                              validators=[InputRequired(message="Doplňte den konce aktivity!")])
    submit = SubmitField('Zaznamenat a odeslat k potvrzení')


class EditActivityPayoffForm(FlaskForm):
    payoff = IntegerField('* Odmena', validators=[InputRequired("Zadejte vysku odmeny!")]) #prelozit
    submit = SubmitField('Potvrdit') #prelozit

class Activities(MethodView):
    @management
    def get(self):
        all_instances = db.fetch_all_by_cls(Activity)
        empl = db.fetch_all_by_cls(Zamestnanec)
        cars = db.fetch_all_by_cls(Vozidlo)
        return render_template('activities.html', all=all_instances, empl=empl, date=datetime.datetime.now().date(),cars=cars, form=EditActivityPayoffForm())


class ActivityAdd(MethodView):
    @norestrict
    def get(self):
        print(NewActivityForm())
        f = NewActivityForm()
        f.vozidlo.choices = db.get_cars_tuples()
        return render_template('activity_new.html', form=f)

    @norestrict
    def post(self):
        actform = NewActivityForm()
        cars = db.get_cars_tuples()
        actform.vozidlo.choices = cars
        instance = db.get_obj_by_clsname(Activity)
        if not actform.validate_on_submit():
            return render_template('activity_new.html', form=actform)
        instance.id_zam = current_user.id_zam
        instance.type = actform.type.data
        instance.id_voz = actform.vozidlo.data
        instance.from_place = actform.from_place.data.encode()
        instance.via_place = actform.via_place.data.encode()
        instance.to_place = actform.to_place.data.encode()
        instance.begin = actform.begin.data
        instance.end = actform.end.data
        db.add(instance)
        flash("Aktivita byla úspěšně odeslána ke schválení!", 'alert alert-success')
        return redirect(url_for('activities-my'))


class ActivityApprove(MethodView):
    @management
    def post(self):
        db.approve_act(request.args.get('id'))
        flash("Aktivita byla úspěšně SCHVÁLENA!", 'alert alert-success')
        return redirect(url_for('activities'))


class ActivityDecline(MethodView):
    @management
    def post(self):
        db.decline_act(request.args.get('id'))
        flash("Aktivita byla úspěšně ZAMÍTNUTA!", 'alert alert-success')
        return redirect(url_for('activities'))


class ActivityDelete(MethodView):
    @management
    def post(self):
        db.delete_act(request.args.get('id'))
        flash("Aktivita byla úspěšně ODSTRANĚNA!", 'alert alert-success')
        return redirect(url_for('activities'))


class ActivityEditPayoff(MethodView):
    @management
    def post(self):
        a = EditActivityPayoffForm()
        if not a.validate_on_submit():
            flash("Zadejte validni cislo odmeny!", 'alert alert-danger')  # prelozit
            return redirect(url_for('activities'))
        df = request.form.get('id')
        print(df)
        db.edit_act_payoff(df, a.payoff.data)
        db.approve_act(request.args.get('id'))
        flash("Aktivita byla úspěšně SCHVÁLENA!", 'alert alert-success')
        return redirect(url_for('activities'))



def configure(app):
    app.add_url_rule('/activities', view_func=Activities.as_view('activities'))
    app.add_url_rule('/activity_add', view_func=ActivityAdd.as_view('activity-add'))
    app.add_url_rule('/activity_approve', view_func=ActivityApprove.as_view('activity-approve'))
    app.add_url_rule('/activity_decline', view_func=ActivityDecline.as_view('activity-decline'))
    app.add_url_rule('/activity_delete', view_func=ActivityDelete.as_view('activity-delete'))
    app.add_url_rule('/activity_e_payoff', view_func=ActivityEditPayoff.as_view('activity-edit-payoff'))

