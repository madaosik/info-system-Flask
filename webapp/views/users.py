from flask import render_template
from flask.views import MethodView
from webapp.core import db

class Users(MethodView):
    def get(self):
        return render_template('users.html')

def configure(app):
    app.add_url_rule('/users', view_func=Users.as_view('users'))