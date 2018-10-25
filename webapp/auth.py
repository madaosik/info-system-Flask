from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, DataRequired, EqualTo, ValidationError
from models import Uzivatel

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[InputRequired(),Email()])
    password = PasswordField('Heslo', validators=[InputRequired()])

class RegistrationForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(),Email()])
    password = PasswordField('Heslo', validators=[DataRequired()])
    password2 = PasswordField('Zopakování hesla', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = Uzivatel.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Použijte, prosím, jinou e-mailovou adresu.')