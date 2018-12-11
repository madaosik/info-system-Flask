from flask import render_template
from flask.views import MethodView
from webapp.core import db
from webapp.roles import admin, employee

class EmplDashboard(MethodView):
    @employee
    def get(self):
        notifications = db.fetch_notifications()
        return render_template('dashboard.html', title='IS - Zaměstnanec', notif=notifications)

class BossDashboard(MethodView):
    @admin
    def get(self):
        approvals_activites = db.fetch_all_pending_approvals()
        approvals_vacation = db.fetch_all_pending_vacation()
        notifications = db.fetch_notifications()
        return render_template('dashboard.html',
                               title='Interní IS dopravní společnosti',
                               act=approvals_activites,
                               vac=approvals_vacation,
                               notif=notifications)

def configure(app):
    app.add_url_rule('/dashboard_boss', view_func=BossDashboard.as_view('dashboard_boss'))
    app.add_url_rule('/dashboard_empl', view_func=EmplDashboard.as_view('dashboard_empl'))


# @app.route('/auth')
# @login_required(roles=[ANY])
# def logged_in():
#     approvals_activites = db.fetch_all_pending_approvals()
#     approvals_vacation = db.fetch_all_pending_vacation()
#     notifications = db.fetch_notifications()
#     return render_template('dashboard.html',
#                            title='Interní IS dopravní společnosti',
#                            act=approvals_activites,
#                            vac=approvals_vacation,
#                            notif=notifications)