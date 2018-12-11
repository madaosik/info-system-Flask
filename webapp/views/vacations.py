from flask import render_template, redirect, url_for, request
from flask.views import MethodView
from webapp.core import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField, PasswordField, SelectField
from wtforms.validators import InputRequired, DataRequired
from wtforms.fields.html5 import DateField
from webapp.roles import admin,current_user,employee,boss

from webapp.core.models import *
from webapp.views.forms import *

from webapp.core import db

import datetime


class Vacations(MethodView):
    def get(self):
        all_instances = db.fetch_all_by_cls(Dovolena_zam_hist)
        empl = db.fetch_all_by_cls(Zamestnanec)
        return render_template('vacations.html', all=all_instances, empl=empl, date=datetime.datetime.now().date())


class VacationsHist(MethodView):
    def get(self):
        all_instances = db.fetch_all_by_cls(Dovolena_zam_hist)
        empl = db.fetch_all_by_cls(Zamestnanec)
        return render_template('vacation_hist.html', all=all_instances, empl=empl, date=datetime.datetime.now().date())


class VacationsHistOne(MethodView):
    def get(self):
        id_zam = request.args.get('id')
        instance = db.fetch_vacation_by_id(id_zam)
        empl = db.fetch_all_by_cls(Zamestnanec)
        check = db.fetch_vacation_by_id(id_zam).first()
        return render_template('vacation_hist_detail.html', empl=empl, me=instance, date=datetime.datetime.now().date(),check=check)


class VacationApprove(MethodView):
    @admin
    def post(self):
        db.approve(Dovolena_zam_hist, request.args.get('id'))  #instance = db.get_obj_by_id(Dovolena_zam_hist, id)
        return redirect(url_for('vacations'))


class VacationDecline(MethodView):
    @admin  # doplnit
    def post(self):
        instance = db.get_obj_by_id(Dovolena_zam_hist, request.args.get('id'))
        db.delete(instance)
        return redirect(url_for('vacations'))



def configure(app):
    app.add_url_rule('/vacations', view_func=Vacations.as_view('vacations'))
    app.add_url_rule('/vacations_decline', view_func=VacationDecline.as_view('vac_decline'))
    app.add_url_rule('/vacations_approve', view_func=VacationApprove.as_view('vac_approve'))
    app.add_url_rule('/vacations_history', view_func=VacationsHist.as_view('vacations_hist'))
    app.add_url_rule('/vacations_history_one', view_func=VacationsHistOne.as_view('vacations_hist_one'))


