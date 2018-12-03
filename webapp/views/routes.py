# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user

from webapp import app
from webapp.views import forms

from webapp.core import db
from webapp.core.auth import login_required, roles_arr, ADMIN, BOSS, USER, ANY
from webapp.core.models import Zamestnanec

import datetime


# ----------- BASIC VIEWS AND MODIFICATIONS ----------------------------

@app.route('/auth/<entity>/new',methods=['GET','POST'])
@login_required(roles=[ADMIN,BOSS,USER])
def pridat(entity):
    db_entity = db.get_db_entity(entity)
    add_form = db_entity['form_class']()
    if add_form.validate_on_submit():
        instance = db.get_obj_by_clsname(db_entity['class'])
        db.update_from_form(instance, add_form)
        if entity == 'dovolena_zaznam':
            instance.id_zam= current_user.id
            instance.celkem = (instance.do - instance.od).days + 1
            db.add(instance)
            return redirect(url_for('show_me', entity=entity, id=current_user.id))
        db.add(instance)
        flash("%s proběhla úspěšně!" % db_entity['add_text'])
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
        flash("%s proběhla úspěšně!" % db_entity['edit_text'])
        return redirect(url_for('show_all', entity=entity))
    return render_template(db_entity['form_page'], action=db_entity['edit_text'], object=instance, form=edit_form)


@app.route('/auth/<entity>/smazat/<id>',methods=['GET','POST'])
@login_required(roles=[ADMIN,BOSS])
def smazat(entity, id):
    db_entity = db.get_db_entity(entity)
    instance = db.get_obj_by_id(db_entity['class'],id)
    db.delete(instance)
    return redirect(url_for('show_all', entity=entity))


@app.route('/auth/<entity>/schvalit/<id>',methods=['GET','POST'])
@login_required(roles=[ADMIN,BOSS])
def schvalit(entity, id):
    db_entity = db.get_db_entity(entity)
    instance = db.get_obj_by_id(db_entity['class'], id)
    db.approve(db_entity['class'], id)
    return redirect(url_for('show_all', entity=entity))


@app.route('/auth/<entity>')
@login_required(roles=[ADMIN,BOSS])
def show_all(entity):
    db_entity = db.get_db_entity(entity)
    all_instances = db.fetch_all_by_cls(db_entity['class'])
    if entity == 'dovolena_zaznam':
        empl= db.fetch_all_by_cls(Zamestnanec)
        return render_template(db_entity['homepage'], all=all_instances, empl=empl)
    return render_template(db_entity['homepage'], all=all_instances)


@app.route('/auth/<entity>/<id>')
@login_required(roles=[USER])
def show_me(entity, id):
    db_entity = db.get_db_entity(entity)
    if entity == 'dovolena_zaznam':
        instance = db.get_obj_by_id_zam(db_entity['class'], id)
    else:
        instance = db.get_obj_by_id(db_entity['class'], id)
    return render_template(db_entity['me_page'], id=id, me=instance)


@app.route('/auth/<entity>/<id>/me',methods=['GET','POST'])
@login_required(roles=[USER])
def upravit_mne(entity, id):
    db_entity = db.get_db_entity(entity)
    instance = db.get_obj_by_id(db_entity['class'],id)
    edit_form = db.get_obj_by_clsname(db_entity['form_class_me'],initobject=instance)
    if edit_form.validate_on_submit():
        db.update_from_form(instance,edit_form)
        return redirect(url_for('show_me', entity=entity, id= id))
    return render_template(db_entity['form_page'], action= 'upravit_mne', object=instance, form=edit_form)


@app.route('/auth/<id>/my_activities',methods=['GET','POST'])
@login_required(roles=[ADMIN,BOSS,USER])
def show_user_activities(id):
    return render_template('user_activities.html')

@app.route('/auth/<id>/my_activities/new',methods=['GET','POST'])
@login_required(roles=[ADMIN,BOSS,USER])
def add_user_activity(id):
    return render_template('new_activity.html')


# ------------ USER MANAGEMENT VIEW FUNCTIONS-----------------


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if current_user.is_authenticated:
        return redirect(url_for('logged_in'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = db.get_user_by_attr(login=form.login.data)
        if user is None:
            error = "Neznámé uživatelské jméno!"
        elif not user.check_password(form.password.data):
            error = "Neplatné heslo!"
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
    reg_form = forms.RegistrationForm()
    if reg_form.validate_on_submit():
        error = db.create_user(reg_form)
        if not error:
            flash('Registrace proběhla úspěšně, přihlašte se, prosím!')
        else:
            return render_template('register.html', title='Registrace uživatele', form=reg_form, error=error)
        return redirect(url_for('login'))
    return render_template('register.html', title='Registrace uživatele', form=reg_form)


@app.route('/auth/uzivatele/new',methods=['GET','POST'])
@login_required(roles=[ADMIN,BOSS])
def pridat_uzivatele():
    user_entity = db.get_db_entity('uzivatele')
    add_form = forms.Uzivatel_form()
    add_form.fill_role_selectbox(roles=roles_arr)
    if add_form.validate_on_submit():
        error = db.create_user(add_form)
        if error:
            return render_template(user_entity['form_page'], action=user_entity['add_text'], form=add_form, error=error)
        else:
            flash("Operace %s proběhla úspěšně!" % user_entity['add_text'])
        return redirect(url_for('show_all', action=user_entity['add_text'], entity='uzivatele', error=error))
    return render_template('uzivatel_form.html', action=user_entity['add_text'], form=add_form)

@app.route('/auth/uzivatele/<id>/uprav', methods=['GET', 'POST'])
@login_required(roles=[ADMIN,BOSS])
def upravit_uzivatele(id):
    user_entity = db.get_db_entity('uzivatele')
    instance = db.get_obj_by_id(user_entity['class'], id)
    edit_form = db.get_obj_by_clsname(user_entity['edit_form_class'], initobject=instance)
    edit_form.fill_role_selectbox(roles=roles_arr)
    if edit_form.validate_on_submit():
        db.edit_user(id,edit_form.data)
        flash("%s proběhla úspěšně!" % user_entity['edit_text'])
        return redirect(url_for('show_all', entity='uzivatele'))
    return render_template(user_entity['form_page'], action=user_entity['edit_text'], object=instance, form=edit_form)


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

# @app.route('/auth/user/uprav/<id>',methods=['GET','POST'])
# @login_required(roles=[ADMIN])
# def edit_user(id):
#     db_entity = db.get_db_entity('uzivatele')
#     user = db.get_obj_by_id(db_entity['class'],id)
#     us = db.get_obj_by_id(db_entity['class'],id)
#     edit_form = db.get_obj_by_clsname(db_entity['form_class'],initobject=instance)
#     user_form = forms.Uzivatel_form(roles_arr)
#     return render_template('uzivatel_form.html', title='Úprava uživatele', user=user, form=user_form)
