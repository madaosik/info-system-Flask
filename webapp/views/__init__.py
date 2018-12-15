from webapp.views import base
from webapp.views import home
from webapp.views import dashboard
from webapp.views import activities
from webapp.views import employees
from webapp.views import medic_visits
from webapp.views import vacations
from webapp.views import cars
from webapp.views import users

def configure_views(app):
    home.configure(app)
    base.configure(app)
    dashboard.configure(app)
    activities.configure(app)
    employees.configure(app)
    medic_visits.configure(app)
    vacations.configure(app)
    cars.configure(app)
    users.configure(app)


