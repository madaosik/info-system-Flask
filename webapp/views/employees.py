from flask import render_template
from flask.views import MethodView
from webapp.core import db

class Employees(MethodView):
    def get(self):
        return render_template('employees.html')

def configure(app):
    app.add_url_rule('/employees', view_func=Employees.as_view('employees'))