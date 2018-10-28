from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Email, DataRequired, EqualTo, ValidationError
from wtforms.fields.html5 import DateField
from webapp.core.models import *

class Zam_form(FlaskForm):
    kr_jmeno = StringField('Křestní jméno', validators=[InputRequired()])
    prijmeni = StringField('Příjmení', validators=[InputRequired()])
    dat_nar = DateField('Datum narození')
    trv_bydliste = StringField('Trvalé bydliště', validators=[InputRequired()])
    prech_bydliste = StringField('Přechodné bydliště')
    telefon = StringField('Telefon')
    email = StringField('E-mail', validators=[Email()])
    prac_sml = StringField('Číslo pracovní sml.')
    aktivni = BooleanField('Aktivní', default='checked')
    submit = SubmitField('Přidat')

    def set_default_values(self, employee=Zamestnanec):
        self.kr_jmeno.default = employee.kr_jmeno
        self.prijmeni.default = employee.prijmeni
        self.dat_nar.default = employee.dat_nar
        self.trv_bydliste.default = employee.trv_bydliste
        self.prech_bydliste.default = employee.prech_bydliste
        self.telefon.default = employee.telefon
        self.email.default = employee.email
        self.prac_sml = employee.prac_sml
        self.aktivni = employee.aktivni
