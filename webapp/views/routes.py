from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user

from webapp import app
from webapp.views import forms

from webapp.core import db
from webapp.core.auth import LoginForm, RegistrationForm, login_required

ADMIN = "admin"
BOSS = "boss"
USER = "user"
ANY = "ANY"

# ----------- BASIC VIEWS AND MODIFICATIONS ----------------------------

@app.route('/auth/<entity>/new',methods=['GET','POST'])
@login_required(roles=[ADMIN,BOSS])
def pridat(entity):
    db_entity = db.get_db_entity(entity)
    add_form = db_entity['form_class']()
    if add_form.validate_on_submit():
        instance = db.get_obj_by_clsname(db_entity['class'])
        add_form.populate_obj(instance)
        db.add(instance)
        return redirect(url_for('show_all', entity=entity))
    return render_template(db_entity['form_page'], action=db_entity['add_text'], form=add_form)

@app.route('/auth/<entity>/uprav/<id>',methods=['GET','POST'])
@login_required(roles=[ADMIN,BOSS])
def upravit(entity, id):
    db_entity = db.get_db_entity(entity)
    instance = db.get_obj_by_id(db_entity['class'],id)
    edit_form = db.get_obj_by_clsname(db_entity['form_class'],initobject=instance)
    if edit_form.validate_on_submit():
        db.update_from_form(instance,edit_form)
        return redirect(url_for('show_all', entity=entity))
    return render_template(db_entity['form_page'], action=db_entity['edit_text'], object=instance, form=edit_form)


@app.route('/auth/<entity>/smazat/<id>',methods=['GET','POST'])
@login_required(roles=[ADMIN,BOSS])
def smazat(entity, id):
    db_entity = db.get_db_entity(entity)
    instance = db.get_obj_by_id(db_entity['class'],id)
    db.delete(instance)
    return redirect(url_for('show_all', entity=entity))


@app.route('/auth/<entity>')
@login_required(roles=[ADMIN,BOSS,USER])
def show_all(entity):
    db_entity = db.get_db_entity(entity)
    all_instances = db.fetch_all_by_cls(db_entity['class'])
    return render_template(db_entity['homepage'], all=all_instances)



# ------------ USER MANAGEMENT VIEW FUNCTIONS-----------------


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if current_user.is_authenticated:
        return redirect(url_for('logged_in'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.get_user_by_login(form.login.data)
        if user is None or not user.check_password(form.password.data):
            error = "Neznámý e-mail nebo neplatné heslo!"
        else:
            login_user(user, remember=form.remember_me.data)
            db.log_visit(user)
            flash("Přihlášení proběhlo úspěšně!")
            return redirect(url_for('logged_in'))
    return render_template('login.html', title='Přihlášení', form=form, error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('logged_in'))
    form = RegistrationForm()
    if form.validate_on_submit():
        db.create_user(login=form.login.data,email=form.email.data,passwd=form.password.data)
        flash('Registrace proběhla úspěšně, přihlašte se, prosím!')
        form = LoginForm()
        return render_template('login.html', title='Přihlášení', form=form)
    return render_template('register.html', title='Registrace uživatele', form=form)

@app.route('/auth')
@login_required(roles=[ANY])
def logged_in():
    approvals_activites = db.fetch_all_pending_approvals()
    approvals_vacation = db.fetch_all_pending_vacation()
    notifications = db.fetch_notifications()
    return render_template('auth_index.html',
                           title='Interní IS dopravní společnosti',
                           act=approvals_activites,
                           vac=approvals_vacation,
                           notif=notifications)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

