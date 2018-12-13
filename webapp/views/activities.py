from flask import render_template,request,redirect,url_for
from flask.views import MethodView
from webapp.core import db
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import InputRequired
import datetime
from webapp.roles import employee, admin, boss,current_user
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


class Activities(MethodView):
    def get(self):
        all_instances = db.fetch_all_by_cls(Activity)
        empl = db.fetch_all_by_cls(Zamestnanec)
        cars = db.fetch_all_by_cls(Vozidlo)
        return render_template('activities.html', all=all_instances, empl=empl, date=datetime.datetime.now().date(),cars=cars)


class ActivityAdd(MethodView):
    @employee
    def get(self):
        print(NewActivityForm())
        f = NewActivityForm()
        f.vozidlo.choices = db. get_cars_tuples()
        return render_template('new_activity.html', form=f)

    @employee
    def post(self):
        actform = NewActivityForm()
        cars = db.get_cars_tuples()
        print(cars)
        actform.vozidlo.choices = cars
        instance = db.get_obj_by_clsname(Activity)
        print(instance)
        print(actform.begin.data)
        #actform.vozidlo=
        if not actform.validate_on_submit():
            return render_template('new_activity.html', form=actform)
        instance.id_zam = current_user.id_zam
        instance.type = actform.type.data
        instance.id_voz = actform.vozidlo.data
        instance.from_place = actform.from_place.data.encode('utf-8')
        instance.via_place = actform.via_place.data.encode('utf-8')
        instance.to_place = actform.to_place.data.encode('utf-8')
        instance.begin = datetime.datetime.now()
        instance.end = datetime.datetime.now()
        print(instance)
        db.add(instance)
        return redirect(url_for('activities'))


def configure(app):
    app.add_url_rule('/activities', view_func=Activities.as_view('activities'))
    app.add_url_rule('/activity_add', view_func=ActivityAdd.as_view('activity-add'))
