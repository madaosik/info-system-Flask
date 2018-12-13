# -*- coding: utf-8 -*-

from flask import Flask, redirect, url_for, session
from flask_login import LoginManager
from webapp.settings import config
import datetime
from webapp.core.auth import configure_login
from webapp.views import configure_views
from webapp.core.models import Uzivatel


def create_app():

    app = Flask(__name__, static_url_path='/static', static_folder='./static')
    app.secret_key = "$tajny_klic#"

    configure_views(app)
    login_manager = LoginManager(app)
    configure_login(app)

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('login'))

    @login_manager.user_loader
    def load_user(id):
        return Uzivatel.query.get(int(id))

    @app.before_request
    def before_request():
        session.permanent = True
        app.permanent_session_lifetime = datetime.timedelta(minutes=10)
        session.modified = True

    return app
