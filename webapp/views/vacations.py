from flask import render_template, redirect, url_for, request, flash
from flask.views import MethodView
import datetime

from webapp.roles import admin, management
from webapp.core.models import *
from webapp.core import db

class Vacations(MethodView):
    @management
    def get(self):
        all_instances = db.fetch_all_by_cls(Dovolena_zam_hist)
        empl = db.fetch_all_by_cls(Zamestnanec)
        return render_template('vacations.html', all=all_instances, empl=empl, date=datetime.datetime.now().date())


class VacationsHist(MethodView):
    @management
    def get(self):
        all_instances = db.fetch_all_by_cls(Dovolena_zam_hist)
        empl = db.fetch_all_by_cls(Zamestnanec)
        return render_template('vacation_hist.html', all=all_instances, empl=empl, date=datetime.datetime.now().date())


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



def configure(app):
    app.add_url_rule('/vacations', view_func=Vacations.as_view('vacations'))
    app.add_url_rule('/vacations_decline', view_func=VacationDecline.as_view('vac_decline'))
    app.add_url_rule('/vacations_approve', view_func=VacationApprove.as_view('vac_approve'))
    app.add_url_rule('/vacations_history', view_func=VacationsHist.as_view('vacations_hist'))
    app.add_url_rule('/vacations_history_one', view_func=VacationsHistOne.as_view('vacations_hist_one'))


