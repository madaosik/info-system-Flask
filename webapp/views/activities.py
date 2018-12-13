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
    
    from_place = StringField('Odkud', default="Brno-Tuřany")
    via_place = StringField('Přes')
    to_place = StringField('Kam', default="Brno-Tuřany")
    submit = SubmitField('Zaznamenat a odeslat k potvrzení')

    def fill_car_selectbox(self, cars):
        self.vozidlo.choices = cars


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
        return render_template('new_activity.html', form=f)

    @employee
    def post(self):
        actform = NewActivityForm()
        instance = db.get_obj_by_clsname(Activity)
        if not actform.validate_on_submit():
            return render_template('vacation_form.html', form=actform)
        db.update_from_form(instance, actform)
        instance.id_zam = current_user.id_zam
        db.add(instance)
        return redirect(url_for('activities'))


def configure(app):
    app.add_url_rule('/activities', view_func=Activities.as_view('activities'))
    app.add_url_rule('/activity_add', view_func=ActivityAdd.as_view('activity-add'))
