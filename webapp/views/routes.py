# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for, flash, session, jsonify
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
            db.insert_vacation(current_user.id_zam, instance.od, instance.do)
            return redirect(url_for('show_mojedovolena', entity=entity, id=current_user.id_zam))
    return render_template(db_entity['form_page'], action=db_entity['add_text'], form=add_form, holidays=get_holidays())


def get_holidays():
    user_vacation = db.get_user_vacation(current_user.id_zam)
    result = []
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    holidays = [[1,1], [30,3], [2,4], [1,5], [8,5], [28,9], [28,10], [17,11], [24,12]]
    for h in holidays[::-1]:
        y = year if month < h[1] else year + 1
        day_no = datetime.date(day=h[0], month=h[1],year=y).weekday()
        if day_no == 1:
            if h[0] == 1 and h[1] == 1:
                continue
            vac_day = datetime.date(day=h[0], month=h[1], year=y) - datetime.timedelta(days=1)
        elif day_no == 3:
            if h[0] == 24 and h[1] == 12:
                continue
            vac_day = datetime.date(day=h[0], month=h[1], year=y) + datetime.timedelta(days=1)
        else:
            continue
        add = True
        for vac in user_vacation:
            if vac_day >= vac.od and vac_day <= vac.do:
                add = False
        if add:
            result.append(vac_day.strftime('%d.%m. %Y'))
    result.sort(key=lambda x: datetime.datetime.strptime(x, '%d.%m. %Y'))
    days = {0: 'Pondělí',4:'Pátek'}
    vac_day = datetime.date(day=27, month=12, year=2018)
    add = True
    for vac in user_vacation:
        if vac_day >= vac.od and vac_day <= vac.do:
            add = False
    christmas = None
    if add:
        christmas = ['27.12. 2018', '31.12. 2018', 3]
    holidays = [[x, days[datetime.datetime.strptime(x, '%d.%m. %Y').weekday()]] for x in result]

    return {'holidays': holidays, 'christmas': christmas}


@app.route('/auth/dovolena_zaznam/quici_insert', methods=["POST"])
def quick_insert_vacation():
    data = request.json
    db.insert_vacation(current_user.id_zam, data['from'], data['to'])
    flash('Dovolená úspěšně přidána', "alert-success")
    return jsonify({})


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
        return render_template(db_entity['homepage'], all=all_instances, empl=empl, date=datetime.datetime.now().date())
    return render_template(db_entity['homepage'], all=all_instances, date=datetime.datetime.now().date())


@app.route('/auth/<entity>/<id>')
@login_required(roles=[USER])
def show_me(entity, id):
    db_entity = db.get_db_entity(entity)
    instance = db.get_obj_by_id(db_entity['class'], id)
    return render_template(db_entity['me_page'], id=id, me=instance)


@app.route('/auth/<entity>/mojedovolena/<id>')
@login_required(roles=[USER])
def show_mojedovolena(entity, id):
    db_entity = db.get_db_entity(entity)
    instance = db.get_obj_by_id_zam(db_entity['class'],id)
    return render_template(db_entity['me_page'], id=id, me=instance, date=datetime.datetime.now().date())

@app.route('/auth/<entity>/historie/all')
@login_required(roles=[ADMIN,BOSS])
def show_vsetkydovolene(entity):
    db_entity = db.get_db_entity(entity)
    all_instances = db.fetch_all_by_cls(db_entity['class'])
    if entity == 'dovolena_zaznam':
        empl= db.fetch_all_by_cls(Zamestnanec)
        return render_template(db_entity['history_page'], all=all_instances, empl=empl, date=datetime.datetime.now().date())
    return render_template(db_entity['homepage'], all=all_instances, date=datetime.datetime.now().date())


@app.route('/auth/<entity>/detaildovolene/<id>')
@login_required(roles=[ADMIN,BOSS])
def show_detaildovolena(entity, id):
    db_entity = db.get_db_entity(entity)
    instance = db.get_obj_by_id_zam(db_entity['class'],id)
    check = db.get_obj_by_id_zam(db_entity['class'],id).first()
    empl = db.get_empl_by_attr(id_zam=id)
    return render_template(db_entity['detail_history_page'], id=id, me=instance, date=datetime.datetime.now().date(),\
                           empl=empl, check=check)


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

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=10)
    session.modified = True

# @app.route('/auth/user/uprav/<id>',methods=['GET','POST'])
# @login_required(roles=[ADMIN])
# def edit_user(id):
#     db_entity = db.get_db_entity('uzivatele')
#     user = db.get_obj_by_id(db_entity['class'],id)
#     us = db.get_obj_by_id(db_entity['class'],id)
#     edit_form = db.get_obj_by_clsname(db_entity['form_class'],initobject=instance)
#     user_form = forms.Uzivatel_form(roles_arr)
#     return render_template('uzivatel_form.html', title='Úprava uživatele', user=user, form=user_form)
