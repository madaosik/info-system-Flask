from flask import render_template
from flask.views import MethodView
from webapp.core import db

class Profile(MethodView):
    def get(self,id_zam):
        print(id_zam)
        return render_template('profile.html')

def configure(app):
    app.add_url_rule('/profile', view_func=Profile.as_view('profile'))