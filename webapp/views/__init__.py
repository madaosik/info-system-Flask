from webapp.views import base
from webapp.views import home
from webapp.views import dashboard
from webapp.views import activities
from webapp.views import activities_my
from webapp.views import employees
from webapp.views import medic_visits
from webapp.views import vacations
from webapp.views import vacation_my
from webapp.views import cars
from webapp.views import users
from webapp.views import employee_profile
from webapp.views import car_profile

def configure_views(app):
    home.configure(app)
    base.configure(app)
    dashboard.configure(app)
    activities.configure(app)
    activities_my.configure(app)
    employees.configure(app)
    medic_visits.configure(app)
    vacations.configure(app)
    vacation_my.configure(app)
    cars.configure(app)
    users.configure(app)
    employee_profile.configure(app)
    car_profile.configure(app)
