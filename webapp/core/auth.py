from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Email, DataRequired, EqualTo, ValidationError
from webapp.core.models import Uzivatel

class LoginForm(FlaskForm):
    login = StringField('Uživatelské jméno', validators=[InputRequired()])
    password = PasswordField('Heslo', validators=[InputRequired()])
    remember_me = BooleanField('Pamatuj si mě')
    submit = SubmitField('Přihlásit se')

class RegistrationForm(FlaskForm):
    login = StringField('Uživatelské jméno', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(),Email()])
    password = PasswordField('Heslo', validators=[DataRequired()])
    password2 = PasswordField('Zopakování hesla', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrace')

    def validate_username(self, login):
        user = Uzivatel.query.filter_by(login=login.data).first()
        if user is not None:
            raise ValidationError('Použijte, prosím, jinou e-mailovou adresu.')