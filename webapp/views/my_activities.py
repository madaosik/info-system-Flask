from flask import render_template
from flask.views import MethodView
from webapp.core import db

class MyActivities(MethodView):
    def get(self,id_zam):
        return render_template('activities.html')

def configure(app):
    app.add_url_rule('/my_activities', view_func=MyActivities.as_view('my_activities'))