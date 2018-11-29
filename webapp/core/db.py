from webapp.core.models import *
from webapp.views.forms import *
#from datetime import datetime
import sqlalchemy as sa


def get_db_entity(i):
    switcher = {
        'zamestnanci': {
            'instance': Zamestnanec(),
            'form': Zam_form(),
            'add_text': "Přidat zaměstnance",
            'edit_text': "Upravit zaměstnance:",
            'homepage_view': "zamestnanci",
            'form_page': "zam_form.html",
        },
        'vozidla': {
            'instance': Vozidlo(),
            'form': Auto_form(),
            'add_text': "Přidat vozidlo",
            'edit_text': "Upravit vozidlo:",
            'homepage_view': "vozidla",
            'form_page': "auto_form.html",
        }
    }
    return switcher.get(i, "Neznámá entita")

# def convert_to_date(formdata):
#     try:
#         dat_nar = datetime.strptime(formdata.get("dat_nar"), '%d.%m.%Y')
#         dat_nar_string = dat_nar.strftime('%Y-%m-%d')
#     except:
#         dat_nar_string = None
#
#     return dat_nar_string

def db_add(object):
    db.session.add(object)
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

def fetch_all_users():
    return Uzivatel.query.all()

def fetch_all_pending_approvals():
    pass

def fetch_all_pending_vacation():
    pass

def fetch_notifications():
    pass