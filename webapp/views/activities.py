from flask import render_template,request,redirect,url_for,flash
from flask_login import current_user
from flask.views import MethodView
from webapp.core import db
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import InputRequired
import datetime
from webapp.roles import employee, admin, management, norestrict
from webapp.core.models import *


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

    def __init__(self,*args,**kwargs):
        super(NewActivityForm,self).__init__(*args, **kwargs)
        self.vozidlo.choices = db.get_cars_tuples()

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        result = True
        if self.begin.data > self.end.data:
            self.end.errors.append('Začátek aktivity musí mít dřívejší datum než její konec!')
            result = False
        return result


class EditActivityPayoffForm(FlaskForm):
    payoff = SelectField('* Odměna', coerce=int, validators=[InputRequired("Zadejte vysku odmeny!")])  # prelozit
    submit = SubmitField('Potvrdit')  # prelozit

    def __init__(self,*args,**kwargs):
        super(EditActivityPayoffForm,self).__init__(*args, **kwargs)
        self.payoff.choices = [(250, '250 Kč'), (500, '500 Kč'), (750, '750 Kč'), (1000, '1000 Kč'), (1500, '1500 Kč')]

class Activities(MethodView):
    @management
    def get(self):
        all_instances = db.fetch_all_by_cls(Activity)
        empl = db.fetch_all_by_cls(Zamestnanec)
        cars = db.fetch_all_by_cls(Vozidlo)
        return render_template('activities.html', all=all_instances, empl=empl, date=datetime.datetime.now(),
                               cars=cars, form=EditActivityPayoffForm())


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
            #print(a.payoff.data)
            #flash("Zadejte validni cislo odmeny!", 'alert alert-danger')  # prelozit
            #return redirect(url_for('activities'))
        df = request.form.get('id')
        db.edit_act_payoff(df, a.payoff.data)
        db.approve_act(df)
        flash("Odměna u aktivity byla úspěšně ZMĚNENA!", 'alert alert-success')
        return redirect(url_for('activities'))


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
        return render_template('activity_new.html', form=f)

    @norestrict
    def post(self):
        actform = NewActivityForm()
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
        return render_template('activity_form_edit.html', form=actform, activity=act)

    @employee
    def post(self):
        id = request.form.get('id')
        editform = NewActivityForm()
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
    app.add_url_rule('/activities', view_func=Activities.as_view('activities'))
    app.add_url_rule('/activity_approve', view_func=ActivityApprove.as_view('activity-approve'))
    app.add_url_rule('/activity_decline', view_func=ActivityDecline.as_view('activity-decline'))
    app.add_url_rule('/activity_delete', view_func=ActivityDelete.as_view('activity-delete'))
    app.add_url_rule('/activity_e_payoff', view_func=ActivityEditPayoff.as_view('activity-edit-payoff'))

    app.add_url_rule('/my_activities', view_func=MyActivities.as_view('activities-my'))
    app.add_url_rule('/activity_add', view_func=ActivityAdd.as_view('activity-add'))
    app.add_url_rule('/activity_edit', view_func=EditMyActivity.as_view('activity-edit'))
    app.add_url_rule('/activity_del_my', view_func=MyActivityDelete.as_view('activity-my-delete'))

