# -*- coding: utf-8 -*-

from webapp.core.models import *
from webapp.views.forms import *
#from datetime import datetime
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
    return classname.query.filter_by(id_zam=id)


def create_user(login,email,passwd):
    user = Uzivatel(login=login, email=email)
    user.set_password(passwd)
    db.session.add(user)
    zam = Zamestnanec(email=email, prijmeni=login)
    db.session.add(zam)
    db.session.commit()

def get_obj_by_clsname(classname,**kwargs):
    if 'initobject' in kwargs:
        instance = classname(obj=kwargs['initobject'])
    else:
        instance = classname()
    return instance

def get_user_by_login(login):
    return Uzivatel.query.filter_by(login=login).first()

def fetch_all_by_cls(classname):
    return classname.query.all()

def add(object):
    db.session.add(object)
    db.session.commit()

def delete(object):
    db.session.delete(object)
    db.session.commit()

def update_from_form(instance,form):
    form.populate_obj(instance)
    db.session.commit()

def add_car(formdata):
    db.session.add(car)
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

def fetch_all_pending_approvals():
    pass

def fetch_all_pending_vacation():
    pass

def fetch_notifications():
    pass