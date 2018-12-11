from flask import render_template
from flask.views import MethodView
from webapp.core import db

class Activities(MethodView):
    def get(self):
        return render_template('activities.html')

def configure(app):
    app.add_url_rule('/activities', view_func=Activities.as_view('activities'))