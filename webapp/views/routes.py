from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user

from webapp import app
from webapp.core.models import Uzivatel

from webapp.core.db import *
from webapp.core.auth import LoginForm, RegistrationForm

@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('zamestnanci'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Uzivatel.query.filter_by(username=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Neznámý e-mail nebo neplatné heslo!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('/zamestnanci'))
    return render_template('login.html', title='Přihlášení', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('/zamestnanci'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/zamestnanci', methods=['GET', 'POST'])
def zamestnanci():
    if request.form:
        if request.form.get('current_id'):
            empl.update(request.form)
        else:
            empl.add(request.form)
    employees = empl.fetch_all()
    return render_template('zamestnanci/zamestnanci.html', employees=employees)


@app.route('/zamestnanci/new')
def pridat_zam():
    return render_template('zamestnanci/pridat_zam.html')

@app.route('/zamestnanci/<id_zam>/upravit_zam',methods=['POST'])
def upravit_zam(id_zam):
    employee = empl.fetch_by_id(id_zam)
    return render_template('zamestnanci/upravit_zam.html', employee=employee)

@app.route('/smazat_zam',methods=['POST'])
def smazat_zam():
    id_zam = request.form.get('id_zam')
    empl.delete(id_zam)
    return redirect("/zamestnanci")
