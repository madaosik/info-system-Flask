from flask import render_template
from flask.views import MethodView
from webapp.core import db

class MedicVisits(MethodView):
    def get(self):
        return render_template('medic_visits.html')

def configure(app):
    app.add_url_rule('/medic_visits', view_func=MedicVisits.as_view('medic_visits'))