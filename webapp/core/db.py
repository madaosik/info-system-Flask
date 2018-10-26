from webapp.core.models import *
from datetime import datetime

def convert_to_date(self, formdata):
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

def fetch_all_zam():
    zam_all = Zamestnanec.query.all()
    return zam_all

def fetch_zam_by_id(id):
    zam = Zamestnanec.query.get(id)
    return zam

def update_zam(formdata):

    zam = Zamestnanec.query.get(formdata.get('current_id'))
    zam.kr_jmeno = formdata.get("kr_jmeno")
    zam.prijmeni = formdata.get("prijmeni")
    zam.trv_bydliste = formdata.get("trv_bydliste")
    zam.prech_bydliste = formdata.get("prech_bydliste")
    zam.telefon = formdata.get("telefon")
    zam.prac_sml = formdata.get("prac_sml")

    dat_nar = convert_to_date(formdata)
    if dat_nar:
        zam.dat_nar = dat_nar

    db.session.commit()

def delete_zam(id):
    zam = Zamestnanec.query.get(id)
    db.session.delete(zam)
    db.session.commit()
