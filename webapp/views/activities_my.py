from flask import render_template
from flask.views import MethodView
from webapp.core import db
from webapp.roles import employee

class MyActivities(MethodView):
    @employee
    def get(self):
        return render_template('activities_my.html')

def configure(app):
    app.add_url_rule('/my_activities', view_func=MyActivities.as_view('activities-my'))