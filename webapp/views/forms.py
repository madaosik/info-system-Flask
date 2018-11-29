from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Email, NumberRange, Optional
from wtforms.fields.html5 import DateField
import datetime

class CzechDateField(DateField):
    """
    Overrides the process_formdata() method definition in a standard DateField
    """
    def process_formdata(self, valuelist):
        if valuelist:
            date_str = ' '.join(valuelist)
            try:
                self.data = datetime.datetime.strptime(date_str, self.format).date()
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Neplatný formát data!'))

class Zam_form(FlaskForm):
    kr_jmeno = StringField('Křestní jméno', validators=[InputRequired(message="Doplňte křestní jméno!")])
    prijmeni = StringField('Příjmení', validators=[InputRequired(message="Doplňte příjmení!")])
    dat_nar = CzechDateField('Datum narození')
    trv_bydliste = StringField('Trvalé bydliště', validators=[InputRequired(message="Doplňte trvalé bydliště!")])
    prech_bydliste = StringField('Přechodné bydliště')
    telefon = StringField('Telefon')
    email = StringField('E-mail', validators=[Email(message="E-mailová adresa nemá správný formát!")])
    prac_sml = StringField('Číslo pracovní sml.')
    aktivni = BooleanField('Aktivní', default='checked')
    submit = SubmitField('Uložit')


class Car_form(FlaskForm):
    spz = StringField('SPZ', validators=[InputRequired("Zadejte SPZ!")])
    znacka = StringField('Značka', validators=[InputRequired("Zadejte značku vozidla!")])
    model = StringField('Model')
    rok_vyroby = IntegerField('Rok výroby', validators=[NumberRange(min=1995,max=2018,message="Zadejte platný rok výroby!")])
    výkon = IntegerField('Výkon(kw)')
    nosnost = IntegerField('Nosnost')
    pocet_naprav = IntegerField('Počet náprav', validators=[NumberRange(min=2,max=10,message="Zadejte počet náprav mezi 2 a 10!")])
    emisni_trida = StringField('Emisní třída')
    submit = SubmitField('Přidat')


