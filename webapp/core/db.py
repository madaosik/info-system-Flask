from webapp.core.models import *
from webapp.views.forms import *
#from datetime import datetime
import sqlalchemy as sa


def get_db_entity(entity_name):
    switcher = {
        'zamestnanci': {
            'class': Zamestnanec,
            'form_class': Zam_form,
            'add_text': "Přidat zaměstnance",
            'edit_text': "Upravit zaměstnance:",
            'homepage': "zamestnanci.html",
            'form_page': "zam_form.html",
        },
        'vozidla': {
            'class': Vozidlo,
            'form_class': Auto_form,
            'add_text': "Přidat vozidlo",
            'edit_text': "Upravit vozidlo:",
            'homepage': "vozidla.html",
            'form_page': "auto_form.html",
        },
        'lekarske_prohlidky': {
            'class': Lekarska_prohl,
            'form_class': Lekar_form,
            'add_text': "Přidat lékařskou prohlídku",
            'edit_text': "Upravit lékařskou prohlídku:",
            'homepage': "lek_prohlidky.html",
            'form_page': "prohl_form.html",
        },
        'uzivatele': {
            'class': Uzivatel,
            'form_class': Lekar_form,
            'edit_text': "Upravit uživatele:",
            'homepage': "users.html",
            'form_page': "uzivatel_form.html",
        },
        'aktivity': {
            'class': Denni_evidence,
            'homepage': "aktivity.html",
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

def get_obj_by_clsname(classname,**kwargs):
    if 'initobject' in kwargs:
        instance = classname(obj=kwargs['initobject'])
    else:
        instance = classname()
    return instance

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