from flask import render_template, redirect, url_for, request, flash
from flask.views import MethodView
from webapp.core import db
import datetime
from webapp.roles import employee, norestrict,current_user
from webapp.core.models import Vozidlo, Activity
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField, DateTimeField, DateTimeLocalField
from wtforms import StringField, SelectField, SubmitField, IntegerField
from wtforms.validators import InputRequired


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


class MyActivities(MethodView):
    @norestrict
    def get(self):
        id_zam = request.args.get('id')
        if id_zam is None:
            id_zam = current_user.id_zam
        act = db.fetch_activity_by_id_zam(id_zam)
        cars = db.fetch_all_by_cls(Vozidlo)
        return render_template('activities_my.html', id=id_zam, me=act, date=datetime.datetime.now(), cars=cars)


class ActivityAdd(MethodView):
    @norestrict
    def get(self):
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
        instance.from_place = actform.from_place.data.encode('utf-8')
        instance.via_place = actform.via_place.data.encode('utf-8')
        instance.to_place = actform.to_place.data.encode('utf-8')
        instance.begin = actform.begin.data
        instance.end = actform.end.data
        db.add(instance)
        flash("Aktivita byla úspěšně odeslána ke schválení!", 'alert alert-success')
        return redirect(url_for('activities-my'))


class EditMyActivity(MethodView):
    @employee
    def get(self):
        a = request.args.get('id')
        act = db.fetch_activity_by_id_act(a)
        actform = NewActivityForm()
        actform.vozidlo.data = act.id_voz
        actform.from_place.data = act.from_place
        actform.via_place.data = act.via_place
        actform.to_place.data = act.to_place
        actform.begin.data = act.begin
        actform.end.data = act.end
        cars = db.get_cars_tuples()
        actform.vozidlo.choices = cars
        return render_template('activity_form_edit.html', form=actform, activity=act)

    @employee
    def post(self):
        id = request.form.get('id')
        editform = NewActivityForm()
        cars = db.get_cars_tuples()
        editform.vozidlo.choices = cars
        activity = db.fetch_activity_by_id_act(id)
        if not editform.validate_on_submit():
            return render_template('activity_form_edit.html', activity=activity, form=editform)
        activity.id_zam = current_user.id_zam
        activity.type = editform.type.data
        activity.id_voz = editform.vozidlo.data
        activity.from_place = editform.from_place.data.encode('utf-8')
        activity.via_place = editform.via_place.data.encode('utf-8')
        activity.to_place = editform.to_place.data.encode('utf-8')
        activity.begin = editform.begin.data
        activity.end = editform.end.data
        activity.seen=False
        activity.approved=False
        db.update_activity_by_id_act(id,activity)
        flash('Úprava aktivity proběhla úspěšně!', 'alert alert-success')
        return redirect(url_for('activities-my'))


class MyActivityDelete(MethodView):
    @norestrict
    def post(self):
        db.delete_act(request.args.get('id'))
        flash("Aktivita byla úspěšně ODSTRANĚNA!", 'alert alert-success')
        return redirect(url_for('activities-my'))


def configure(app):
    app.add_url_rule('/my_activities', view_func=MyActivities.as_view('activities-my'))
    app.add_url_rule('/activity_add', view_func=ActivityAdd.as_view('activity-add'))
    app.add_url_rule('/activity_edit', view_func=EditMyActivity.as_view('activity-edit'))
    app.add_url_rule('/activity_del_my', view_func=MyActivityDelete.as_view('activity-my-delete'))
