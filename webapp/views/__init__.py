from webapp.views import base
from webapp.views import home
from webapp.views import dashboard
from webapp.views import activities
from webapp.views import my_activities
from webapp.views import employees
from webapp.views import medic_visits
from webapp.views import vacations
from webapp.views import my_vacation
from webapp.views import cars
from webapp.views import users
from webapp.views import profile

def configure_views(app):
    home.configure(app)
    base.configure(app)
    dashboard.configure(app)
    activities.configure(app)
    my_activities.configure(app)
    employees.configure(app)
    medic_visits.configure(app)
    vacations.configure(app)
    my_vacation.configure(app)
    cars.configure(app)
    users.configure(app)
    profile.configure(app)
