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
        log_visit(user)
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
    employees = Zamestnanec.query.all()
    return render_template('zamestnanci.html', employees=employees)


@app.route('/auth/<entity>/new',methods=['GET','POST'])
@login_required
def pridat(entity):
    if entity=='zamestnanci':
        add_form = Zam_form()
    if add_form.validate_on_submit():
        employee = Zamestnanec()
        add_form.populate_obj(employee)
        db.session.add(employee)
        db.session.commit()
        return redirect(url_for('zamestnanci'))
    return render_template('zam_form.html', action="Přidat zaměstnance", form=add_form)

@app.route('/auth/<entity>/uprav/<id>',methods=['GET','POST'])
@login_required
def upravit(entity, id):
    if entity == 'zamestnanci':
        employee = Zamestnanec.query.get(id)
        edit_form = Zam_form(obj=employee)
    if edit_form.validate_on_submit():
        edit_form.populate_obj(employee)
        db.session.commit()
        return redirect(url_for('zamestnanci'))
    return render_template('zam_form.html', action="Upravit zaměstnance:", empl=employee, form=edit_form)


@app.route('/auth/<entity>/smazat/<id>',methods=['GET','POST'])
@login_required
def smazat(entity, id):
    if entity == 'zamestnanci':
        zam = Zamestnanec.query.get(id)
        db.session.delete(zam)
        db.session.commit()
        return redirect("/auth/zamestnanci")

@app.route('/auth/vozidla', methods=['GET', 'POST'])
@login_required
def vozidla():
    cars = Vozidlo.query.all()
    return render_template('vozidla.html', cars=cars)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/users')
@login_required
def user_maintenance():
    users = Uzivatel.query.all()
    return render_template('users.html', users=users)


@app.route('/lek_prohlidky')
@login_required
def lek_prohlidky():
    return render_template('lek_prohlidky.html')