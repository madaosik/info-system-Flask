# -*- coding: utf-8 -*-

from webapp.core.models import *
from webapp.views.forms import *
from webapp.core.auth import roles_arr
#from datetime import datetime
from sqlalchemy import desc
import sqlalchemy as sa


def get_db_entity(entity_name):
    switcher = {
        'zamestnanci': {
            'class': Zamestnanec,
            'form_class': Zam_form,
            'form_class_me': Zam_form_ja,
            'add_text': "Přidat zaměstnance",
            'edit_text': "Úprava zaměstnance",
            'homepage': "zamestnanci.html",
            'form_page': "zam_form.html",
            'me_page': "show_me.html",
        },
        'vozidla': {
            'class': Vozidlo,
            'form_class': Auto_form,
            'add_text': "Přidat vozidlo",
            'edit_text': "Úprava vozidla",
            'homepage': "vozidla.html",
            'form_page': "auto_form.html",
        },
        'lekarske_prohlidky': {
            'class': Lekarska_prohl,
            'form_class': Lekar_form,
            'add_text': "Přidat lékařskou prohlídku",
            'edit_text': "Úprava lékařské prohlídky",
            'homepage': "lek_prohlidky.html",
            'form_page': "prohl_form.html",
        },
        'uzivatele': {
            'class': Uzivatel,
            'form_class': Uzivatel_form,
            'edit_form_class': Uzivatel_edit_form,
            'form_init': roles_arr,
            'add_text': "Přidat uživatele",
            'edit_text': "Úprava uživatele",
            'homepage': "users.html",
            'form_page': "uzivatel_form.html",
        },
        'aktivity': {
            'class': Denni_evidence,
            'homepage': "aktivity.html",
        },
        'dovolena': {
            'class': Dovolena_zam,
            'form_class': Dovo_form,
            'homepage': 'dovolena.html',

        },
        'dovolena_zaznam': {
            'class': Dovolena_zam_hist,
            'form_class': Dovo_zaz_form,
            'add_text': "Přidat dovolenou",
            'homepage': 'dovolena.html',
            'form_page': "dovo_zam_form.html",
            'me_page': 'dovolena_zamestnanec.html',
            'history_page': 'dovolena_historie.html',
            'detail_history_page': 'dovolena_historie_detail.html',
        }

    }
    return switcher.get(entity_name, "Neznámá entita")

# def convert_to_date(formdata):
#     try:
#         dat_nar = datetime.strptime(formdata.get("dat_nar"), '%d.%m.%Y')
#         dat_nar_string = dat_nar.strftime('%Y-%m-%d')
#     except:
#         dat_nar_string = None
#
#     return dat_nar_string


def get_obj_by_id(classname,id):
    return classname.query.get(id)


def get_obj_by_id_zam(classname, id):
    return classname.query.filter_by(id_zam=id).all()


def get_user_by_attr(**kwargs):
    if 'login' in kwargs:
        user = Uzivatel.query.filter_by(login=kwargs['login']).first()
    elif 'id' in kwargs:
        user = Uzivatel.query.get(kwargs['id'])
    return user


def get_empl_by_attr(**kwargs):
    if 'email' in kwargs:
        user = Zamestnanec.query.filter_by(email=kwargs['email']).first()
    elif 'id_zam' in kwargs:
        user = Zamestnanec.query.filter_by(id_zam=kwargs['id_zam']).first()
    return user


def check_login_and_email(login,email):
    error = None
    if get_user_by_attr(login=login) is not None:
        error = "Použijte, prosím, jiné uživatelské jméno. %s již existuje!" % login
        return error

    empl = get_empl_by_attr(email=email)
    if empl:
        if Uzivatel.query.filter_by(id_zam=empl.id_zam).first() is not None:
            error = "Uživatelský účet spojený s e-mailem %s již existuje. Kontaktujte správce!" % email
    else:
        error = "Zaměstnanec s e-mailem %s není veden v databázi. Kontaktujte správce!" % email

    if error:
        return error
    else:
        return empl.id_zam


def create_user(form):
    id_zam = check_login_and_email(login=form.login.data, email=form.email.data)
    if not isinstance(id_zam,int):
        return id_zam
    try:
        user = Uzivatel(login=form.login.data, role=form.role.data, id_zam=id_zam)
    except AttributeError:
        user = Uzivatel(login=form.login.data, id_zam=id_zam)

    try:
        user.set_password(form.password.data)
    except AttributeError:
        pass

    db.session.add(user)
    db.session.commit()


def edit_user(id,form_data_dict):
    user = get_user_by_attr(id=id)
    user.role = form_data_dict['role']

    if form_data_dict['password']:
        user.set_password(form_data_dict['password'])
    db.session.commit()


def get_obj_by_clsname(classname,**kwargs):
    if 'initobject' in kwargs:
        instance = classname(obj=kwargs['initobject'])
    else:
        instance = classname()
    return instance


def fetch_all_by_cls(classname):
    if classname == Zamestnanec:
        return classname.query.order_by('prijmeni')
    elif classname == Dovolena_zam_hist:
        return classname.query.order_by('od')
    return classname.query.all()


def add(object):
    db.session.add(object)
    db.session.commit()


def delete(object):
    db.session.delete(object)
    db.session.commit()


def approve(classname, id):
    q = classname.query.get(id)
    q.potvrzeni = True
    db.session.commit()


def update_from_form(instance,form):
    form.populate_obj(instance)
    db.session.commit()


def log_visit(user=Uzivatel):
    target = Uzivatel.query.get(user.id)
    if not target.poc_prihl:
        visit_cnt = 1
    else:
        visit_cnt = target.poc_prihl + 1

    target.poc_prihl = visit_cnt
    target.posl_prihl = sa.func.current_timestamp()
    db.session.commit()

def get_cars_tuples():
    cars = Vozidlo.query.all()
    car_tuples_arr = []
    for car in cars:
        car_string = "%s: %s %s" % (car.spz, car.znacka, car.model)
        car_tuples_arr.append((car.id_voz, car_string))
    return car_tuples_arr

def fetch_all_pending_approvals():
    pass


def fetch_all_pending_vacation():
    return Dovolena_zam_hist.query.filter_by(potvrzeni=False).first()


def fetch_notifications():
    pass


def insert_vacation(user_id, date_from, date_to):
    date_from = datetime.datetime.strptime(date_from, '%d.%m. %Y')
    date_to = datetime.datetime.strptime(date_to, '%d.%m. %Y')
    stmt = Dovolena_zam_hist(id_zam=user_id, od=date_from, do=date_to, celkem=(date_to - date_from).days + 1)
    db.session.add(stmt)
    db.session.commit()

def get_user_vacation(uid):
    return db.session.query(Dovolena_zam_hist).filter_by(id_zam=uid).all()