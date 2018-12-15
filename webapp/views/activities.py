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


class EditActivityPayoffForm(FlaskForm):
    payoff = SelectField('* Odmena', coerce=int, validators=[InputRequired("Zadejte vysku odmeny!")],
                             choices=[(100, "100"), (500, '500')])  # prelozit
    submit = SubmitField('Potvrdit')  # prelozit


class Activities(MethodView):
    @management
    def get(self):
        all_instances = db.fetch_all_by_cls(Activity)
        empl = db.fetch_all_by_cls(Zamestnanec)
        cars = db.fetch_all_by_cls(Vozidlo)
        return render_template('activities.html', all=all_instances, empl=empl, date=datetime.datetime.now().date(),cars=cars, form=EditActivityPayoffForm())


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
        print(a.payoff.data)
        db.edit_act_payoff(df, a.payoff.data)
        db.approve_act(df)
        flash("Aktivita byla úspěšně SCHVÁLENA!", 'alert alert-success')
        return redirect(url_for('activities'))



def configure(app):
    app.add_url_rule('/activities', view_func=Activities.as_view('activities'))
    app.add_url_rule('/activity_approve', view_func=ActivityApprove.as_view('activity-approve'))
    app.add_url_rule('/activity_decline', view_func=ActivityDecline.as_view('activity-decline'))
    app.add_url_rule('/activity_delete', view_func=ActivityDelete.as_view('activity-delete'))
    app.add_url_rule('/activity_e_payoff', view_func=ActivityEditPayoff.as_view('activity-edit-payoff'))

