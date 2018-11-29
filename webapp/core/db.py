from webapp.core.models import *
from datetime import datetime
import sqlalchemy as sa

def convert_to_date(formdata):
    try:
        dat_nar = datetime.strptime(formdata.get("dat_nar"), '%d.%m.%Y')
        dat_nar_string = dat_nar.strftime('%Y-%m-%d')
    except:
        dat_nar_string = None

    return dat_nar_string

def add_zam(formdata):
    zam = Zamestnanec(
        kr_jmeno=formdata.get("kr_jmeno"),
        prijmeni=formdata.get("prijmeni"),
        trv_bydliste=formdata.get("trv_bydliste"),
        prech_bydliste=formdata.get("prech_bydliste"),
        telefon=formdata.get("telefon"),
        prac_sml=formdata.get("prac_sml")
    )

    dat_nar_string = convert_to_date(formdata)
    if dat_nar_string:
        zam.dat_nar = dat_nar_string

    db.session.add(zam)
    db.session.commit()


def add_car(formdata):
    car = Vozidlo(
        spz=formdata.get("spz"),
        znacka=formdata.get("znacka"),
        model=formdata.get("model"),
        rok_vyroby=formdata.get("rok_vyroby"),
        vykon=formdata.get("vykon"),
        nosnost=formdata.get("nosnost"),
        pocet_naprav=formdata.get("pocet_naprav"),
        emisni_trida = formdata.get("emisni_trida"),
    )
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