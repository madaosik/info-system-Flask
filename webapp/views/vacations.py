from flask import render_template
from flask.views import MethodView
from webapp.core import db

class Vacations(MethodView):
    def get(self):
        return render_template('vacations.html')

def configure(app):
    app.add_url_rule('/vacations', view_func=Vacations.as_view('vacations'))