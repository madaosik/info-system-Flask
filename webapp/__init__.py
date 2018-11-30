# -*- coding: utf-8 -*-

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from webapp.settings import config

app = Flask(__name__)

app.config.from_object(config)
Bootstrap(app)

db = SQLAlchemy(app)
db.init_app(app)

login = LoginManager(app)
login.login_view = 'login'

from webapp.views import routes
