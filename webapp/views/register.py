from flask_wtf import FlaskForm
from flask import redirect, render_template, url_for, request, flash
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email
from flask.views import MethodView

from webapp.core import db

class RegistrationForm(FlaskForm):
    login = StringField('Uživatelské jméno', validators=[DataRequired(message="Zadejte uživatelské jméno")])
    email = StringField('E-mail', validators=[DataRequired(),Email(message="Nepovolený tvar e-mailové adresy!")])
    password = PasswordField('Heslo', validators=[DataRequired(message="Zadejte heslo!")])
    password2 = PasswordField('Zopakování hesla', validators=[DataRequired(), EqualTo('password',message="Zadaná hesla se neshodují!")])
    submit = SubmitField('Registrace')

class Register(MethodView):
    def get(self):
        if current_user.is_authenticated():
            return redirect(url_for('logged_in'))
        return render_template('register.html', title='Registrace uživatele', form=RegistrationForm())

    def post(self):
        form = RegistrationForm(request.form)
        if not form.validate_on_submit():
            return render_template('register.html', title='Registrace uživatele', form=form)
        error = db.create_user(form)
        if error:
            return render_template('register.html', title='Registrace uživatele', form=form, error=error)
        else:
            flash('Registrace proběhla úspěšně, přihlašte se, prosím!', 'alert-success')
            return redirect(url_for('login'))


def configure(app):
    app.add_url_rule('/register', view_func=Register.as_view('register'))
