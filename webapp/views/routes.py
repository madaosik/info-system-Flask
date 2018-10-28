from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, login_required, logout_user

from webapp import app
from webapp.core.models import Uzivatel
from webapp.views.forms import *

from webapp.core.db import *
from webapp.core.auth import LoginForm, RegistrationForm

@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('logged_in'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Uzivatel.query.filter_by(login=form.login.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Neznámý e-mail nebo neplatné heslo!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('logged_in'))
    return render_template('login.html', title='Přihlášení', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('logged_in'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Uzivatel(login=form.login.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/auth')
@login_required
def logged_in():
    approvals_activites = fetch_all_pending_approvals()
    approvals_vacation = fetch_all_pending_vacation()
    notifications = fetch_notifications()
    return render_template('auth_index.html',
                           title='Interní IS dopravní společnosti',
                           act=approvals_activites,
                           vac=approvals_vacation,
                           notif=notifications)

@app.route('/auth/zamestnanci', methods=['GET', 'POST'])
@login_required
def zamestnanci():
    if request.form:
        if request.form.get('current_id'):
            update_zam(request.form)
        else:
            add_zam(request.form)
    employees = fetch_all_zam()
    return render_template('zamestnanci.html', employees=employees)


@app.route('/auth/zamestnanci/new')
@login_required
def pridat_zam():
    form = Zam_form()
    return render_template('pridat_zam.html', form=form)

@app.route('/auth/zamestnanci/<id_zam>/upravit_zam',methods=['POST'])
@login_required
def upravit_zam(id_zam):
    employee = fetch_zam_by_id(id_zam)
    form = Zam_form()
    form.set_default_values(employee)
    return render_template('upravit_zam.html', employee=employee, form=form)

@app.route('/auth/smazat_zam',methods=['POST'])
@login_required
def smazat_zam():
    id_zam = request.form.get('id_zam')
    delete_zam(id_zam)
    return redirect("/auth/zamestnanci")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))