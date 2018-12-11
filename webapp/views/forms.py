# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField, PasswordField, SelectField
from wtforms.validators import InputRequired, DataRequired, Email, NumberRange, ValidationError, EqualTo
from wtforms.fields.html5 import DateField, DateTimeField, DateTimeLocalField
import datetime

from webapp.views.register import RegistrationForm

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
    kr_jmeno = StringField('* Křestní jméno', validators=[InputRequired(message="Doplňte křestní jméno!")])
    prijmeni = StringField('* Příjmení', validators=[InputRequired(message="Doplňte příjmení!")])
    dat_nar = CzechDateField('Datum narození')
    trv_bydliste = StringField('Trvalé bydliště')
    prech_bydliste = StringField('Přechodné bydliště')
    telefon = StringField('Telefon')
    email = StringField('* E-mail', validators=[Email(message="E-mailová adresa nemá správný formát!")])
    prac_sml = StringField('Číslo pracovní sml.')
    aktivni = BooleanField('Aktivní', default='checked')
    submit = SubmitField('Uložit')

class Zam_form_ja(FlaskForm):
    trv_bydliste = StringField('Trvalé bydliště')
    prech_bydliste = StringField('Přechodné bydliště')
    telefon = StringField('Telefon')
    email = StringField('* E-mail', validators=[Email(message="E-mailová adresa nemá správný formát!")])
    submit = SubmitField('Uložit')

# class Auto_form(FlaskForm):
#     spz = StringField('* SPZ', validators=[InputRequired("Zadejte SPZ!")])
#     znacka = StringField('* Značka', validators=[InputRequired("Zadejte značku vozidla!")])
#     model = StringField('Model')
#     rok_vyroby = IntegerField('* Rok výroby', validators=[NumberRange(min=1995,max=2018,message="Zadejte platný rok výroby!")])
#     vykon = IntegerField('Výkon(kw)')
#     nosnost = IntegerField('Nosnost')
#     pocet_naprav = IntegerField('* Počet náprav', validators=[NumberRange(min=2,max=10,message="Zadejte počet náprav mezi 2 a 10!")])
#     emisni_trida = StringField('Emisní třída')
#     submit = SubmitField('Uložit')


class User_form(FlaskForm):
    login = StringField('* Uživatelské jméno', validators=[InputRequired(message="Doplňte uživatelské jméno!")])


#class Dovo_form(FlaskForm):
#    dat_od = CzechDateField('Datum začátku', validators=[InputRequired(message="Doplňte datum začátku dovolené!")])
 #   dat_do = CzechDateField('Datum konce', validators=[InputRequired(message="Doplňte datum konce dovolené!")])


#class Dovo_zaz_form(FlaskForm):
   # od = CzechDateField('Datum začátku', validators=[InputRequired(message="Doplňte datum začátku dovolené!")])
   # do = CzechDateField('Datum konce (včetně)', validators=[InputRequired(message="Doplňte datum konce dovolené!")])
   # submit = SubmitField('Uložit')

#    def validate(self):
#        if not FlaskForm.validate(self):
#            return False
#        result = True
#       if self.od.data > self.do.data:
#            self.od.errors.append('Začátek dovolené musí mít dřívejší datum než její konec!')
  #          result = False
  #      return result


class Lekar_form(FlaskForm):
    pass

class Uzivatel_form(RegistrationForm):
    role = SelectField('Role')
    submit = SubmitField('Uložit')

    def fill_role_selectbox(self, roles):
        self.role.choices = roles

class Uzivatel_edit_form(Uzivatel_form):
    # Heslo při editaci nechceme jako povinné pole a login nejde měnit.....
    email = None
    login = None
    password = PasswordField('Heslo')
    password2 = PasswordField('Zopakování hesla',validators=[EqualTo('password', message="Zadaná hesla se neshodují!")])
    role = SelectField('Role')
    submit = SubmitField('Uložit')

class New_activity_form(FlaskForm):

    vozidlo = SelectField('Vozidlo')
    misto_z = StringField('Odkud', default="Brno-Tuřany")
    misto_pres = StringField('Přes')
    misto_kam = StringField('Kam', default="Brno-Tuřany")
    datum_od = DateTimeLocalField('Datum a čas odjezdu', default=datetime.datetime.now, format="%Y-%m-%dT%H:%M",
                              validators=[InputRequired(message="Doplňte den začátku aktivity!")])
    datum_do = DateTimeLocalField('Datum a čas návratu', default=datetime.datetime.now, format="%Y-%m-%dT%H:%M",
                              validators=[InputRequired(message="Doplňte den konce aktivity!")])
    submit = SubmitField('Zaznamenat a odeslat k potvrzení')

    def fill_car_selectbox(self, cars):
        self.vozidlo.choices = cars
