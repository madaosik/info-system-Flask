from flask import render_template
from flask.views import MethodView
from webapp.core import db

class MyVacation(MethodView):
    def get(self,id_zam):
        return render_template('my_vacation.html')

def configure(app):
    app.add_url_rule('/my_vacation', view_func=MyVacation.as_view('my_vacation'))