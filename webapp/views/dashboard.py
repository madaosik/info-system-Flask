from flask import render_template
from flask.views import MethodView
from webapp.core import db
from webapp.roles import admin, employee, management, current_user

class EmplDashboard(MethodView):
    @employee
    def get(self):
        vacations = db.fetch_unseen_zam_vacation(current_user.id_zam)
        act = db.fetch_unseen_zam_activity(current_user.id_zam)
        return render_template('dashboard.html', title='IS - Zaměstnanec', notif_vac=vacations, notif_act=act)


class BossDashboard(MethodView):
    @management
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
    app.add_url_rule('/dashboard-boss', view_func=BossDashboard.as_view('dashboard-boss'))
    app.add_url_rule('/dashboard-empl', view_func=EmplDashboard.as_view('dashboard-empl'))

