# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for, flash, session
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
        db.add(instance)
        flash("Operace %s proběhla úspěšně!" % db_entity['add_text'])
        return redirect(url_for('show_all', entity=entity))
    return render_template(db_entity['form_page'], action=db_entity['add_text'], form=add_form)


@app.route('/auth/<entity>/newreq',methods=['GET','POST'])
@login_required(roles=[ADMIN,BOSS,USER])
def pridat_ziadost(entity):
    db_entity = db.get_db_entity(entity)
    add_form = db_entity['form_class']()
    if add_form.validate_on_submit():
        instance = db.get_obj_by_clsname(db_entity['class'])
        db.update_from_form(instance, add_form)
        if entity == 'dovolena_zaznam':
            instance.id_zam = current_user.id_zam
            instance.celkem = (instance.do - instance.od).days + 1
            db.add(instance)
            return redirect(url_for('show_mojedovolena', entity=entity, id=current_user.id_zam))

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


#@app.route('/auth/<entity>/schvalit/<id>',methods=['GET','POST'])
#@login_required(roles=[ADMIN,BOSS])
#def schvalit(entity, id):
#    db_entity = db.get_db_entity(entity)
#    instance = db.get_obj_by_id(db_entity['class'], id)
#    db.approve(db_entity['class'], id)
#    return redirect(url_for('show_all', entity=entity))


@app.route('/auth/<entity>')
@login_required(roles=[ADMIN,BOSS])
def show_all(entity):
    db_entity = db.get_db_entity(entity)
    all_instances = db.fetch_all_by_cls(db_entity['class'])
    if entity == 'dovolena_zaznam':
        empl= db.fetch_all_by_cls(Zamestnanec)
        return render_template(db_entity['homepage'], all=all_instances, empl=empl, date=datetime.datetime.now().date())
    return render_template(db_entity['homepage'], all=all_instances, date=datetime.datetime.now().date())


@app.route('/auth/<entity>/<id>')
@login_required(roles=[USER])
def show_me(entity, id):
    db_entity = db.get_db_entity(entity)
    instance = db.get_obj_by_id(db_entity['class'], id)
    return render_template(db_entity['me_page'], id=id, me=instance)


#@app.route('/auth/<entity>/mojedovolena/<id>')
#@login_required(roles=[USER])
#def show_mojedovolena(entity, id):
#    db_entity = db.get_db_entity(entity)
#    instance = db.get_obj_by_id_zam(db_entity['class'],id)
#    return render_template(db_entity['me_page'], id=id, me=instance, date=datetime.datetime.now().date())

#@app.route('/auth/<entity>/historie/all')
#@login_required(roles=[ADMIN,BOSS])
#def show_vsetkydovolene(entity):
#    db_entity = db.get_db_entity(entity)
#    all_instances = db.fetch_all_by_cls(db_entity['class'])
#    if entity == 'dovolena_zaznam':
#        empl= db.fetch_all_by_cls(Zamestnanec)
#        return render_template(db_entity['history_page'], all=all_instances, empl=empl, date=datetime.datetime.now().date())
#    return render_template(db_entity['homepage'], all=all_instances, date=datetime.datetime.now().date())


@app.route('/auth/<entity>/detaildovolene/<id>')
@login_required(roles=[ADMIN,BOSS])
#def show_detaildovolena(entity, id): vacHistOne
#    db_entity = db.get_db_entity(entity)
#    instance = db.get_obj_by_id_zam(db_entity['class'],id)
#    check = db.get_obj_by_id_zam(db_entity['class'],id).first()
#    empl = db.get_empl_by_attr(id_zam=id)
#    return render_template(db_entity['detail_history_page'], id=id, me=instance, date=datetime.datetime.now().date(),\
#                           empl=empl, check=check)


@app.route('/auth/<entity>/<id>/me',methods=['GET','POST'])
@login_required(roles=[USER])
def upravit_mne(entity, id):
    db_entity = db.get_db_entity(entity)
    instance = db.get_obj_by_id(db_entity['class'], id)
    edit_form = db.get_obj_by_clsname(db_entity['form_class_me'],initobject=instance)
    if edit_form.validate_on_submit():
        db.update_from_form(instance,edit_form)
        return redirect(url_for('show_me',entity= 'zamestnanci', id= id))
    return render_template(db_entity['form_page'], action= 'upravit_mne', object=instance, form=edit_form)


@app.route('/auth/<id>/my_activities',methods=['GET','POST'])
@login_required(roles=[ADMIN,BOSS,USER])
def show_user_activities(id):
    return render_template('user_activities.html')

@app.route('/auth/<id>/my_activities/new',methods=['GET','POST'])
@login_required(roles=[ADMIN,BOSS,USER])
def add_user_activity(id):
    activity_form = forms.New_activity_form()
    activity_form.fill_car_selectbox(db.get_cars_tuples())
    return render_template('new_activity.html', form=activity_form)


# ------------ USER MANAGEMENT VIEW FUNCTIONS-----------------



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

