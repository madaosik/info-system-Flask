from flask import render_template, redirect, url_for
from flask.views import MethodView


class Home(MethodView):
    def get(self):
        return redirect(url_for('login'))

def configure(app):
    app.add_url_rule('/home',view_func=Home.as_view('home'))