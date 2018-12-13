# -*- coding: utf-8 -*-

from webapp.core.models import *
from webapp.roles import roles
import sqlalchemy as sa
from webapp.core.db_connector import session


def get_obj_by_id(classname,id):
    return classname.query.get(id)


def get_obj_by_id_zam(classname, id):
    return classname.query.filter_by(id_zam=id)


def get_user_by_attr(**kwargs):
    if 'login' in kwargs:
        user = Uzivatel.query.filter_by(login=kwargs['login']).first()
    elif 'id' in kwargs:
        user = Uzivatel.query.get(kwargs['id'])
    return user


def get_empl_by_attr(**kwargs):
    if 'email' in kwargs:
        user = Zamestnanec.query.filter_by(email=kwargs['email']).first()
    elif 'id_zam' in kwargs:
        user = Zamestnanec.query.filter_by(id_zam=kwargs['id_zam']).first()
    return user


def is_login_valid(login):
    return False if get_user_by_attr(login=login) is not None else True

def create_user(form):
    id_zam = check_login_and_email(login=form.login.data, email=form.email.data)
    if not isinstance(id_zam,int):
        return id_zam
    try:
        user = Uzivatel(login=form.login.data, role=form.role.data, id_zam=id_zam)
    except AttributeError:
        user = Uzivatel(login=form.login.data, id_zam=id_zam)

    try:
        user.set_password(form.password.data)
    except AttributeError:
        pass

    session.add(user)
    session.commit()


def edit_user_from_form(id,form_data_dict):
    user = get_user_by_attr(id=id)

    try:
        user.role = form_data_dict['role']
    except KeyError:
        pass
    if form_data_dict['password']:
        user.set_password(form_data_dict['password'])
    if form_data_dict['login']:
        user.login = form_data_dict['login']
    session.commit()

def user_create(employee_id):
    login = "xuser"
    if not is_login_valid(login):
        for i in range(1,99):
            login = login + str(i)
            if is_login_valid(login):
                break

    user = Uzivatel(login=login,id_zam=employee_id)
    user.set_password("1234")
    session.add(user)
    session.commit()
    return login

def first_login_edit(id,form_data_dict):
    user

def get_obj_by_clsname(classname,**kwargs):
    if 'initobject' in kwargs:
        instance = classname(obj=kwargs['initobject'])
    else:
        instance = classname()
    return instance


def fetch_all_by_cls(classname):
    if classname == Zamestnanec:
        return classname.query.order_by('prijmeni')
    elif classname == Dovolena_zam_hist:
        return classname.query.order_by('od')
    return classname.query.all()


def add(object):
    session.add(object)
    session.commit()

def add_employee(employee):
    session.add(employee)
    session.commit()
    return employee.id_zam

def delete(object):
    session.delete(object)
    session.commit()

def delete_car(id):
    session.query(Vozidlo).filter_by(id_voz=id).delete()
    session.commit()


def approve(classname, id):
    q = classname.query.get(id)
    q.potvrzeni = True
    session.commit()


def update_from_form(instance,form):
    form.populate_obj(instance)
    session.commit()


def log_visit(user=Uzivatel):
    target = Uzivatel.query.get(user.id)
    if not target.poc_prihl:
        visit_cnt = 1
    else:
        visit_cnt = target.poc_prihl + 1

    target.poc_prihl = visit_cnt
    target.posl_prihl = sa.func.current_timestamp()
    session.commit()

def get_cars_tuples():
    cars = Vozidlo.query.all()
    car_tuples_arr = []
    for car in cars:
        car_string = "%s: %s %s" % (car.spz, car.znacka, car.model)
        car_tuples_arr.append((car.id_voz, car_string))
    return car_tuples_arr


def fetch_all_pending_approvals():
    pass


def fetch_all_pending_vacation():
    return Dovolena_zam_hist.query.filter_by(potvrzeni=False).first()


def fetch_notifications():
    pass

def fetch_car(id):
    return Vozidlo.query.filter_by(id_voz=id).first()


def fetch_all_cars():
    return Vozidlo.query.all()


#Vacation functions

def fetch_all_vacations():
    return Dovolena_zam_hist.query.all()


def fetch_vacation_by_id(id):
    return Dovolena_zam_hist.query.filter_by(id_zam=id)

# Employee functions

def delete_employee(id):
    session.query(Zamestnanec).filter_by(id_zam=id).delete()
    session.commit()

def fetch_employee_by_id(id):
    return Zamestnanec.query.filter_by(id_zam=id).first()

# User functions

def fetch_user_tuples():
    return (session.query(Uzivatel, Zamestnanec).filter(Uzivatel.id_zam == Zamestnanec.id_zam).all())


def get_employee_tuples():
    employees = Zamestnanec.query.all()
    empl_tuples_arr = []
    for employee in employees:
        employee_string = "%s %s" % (employee.kr_jmeno, employee.prijmeni)
        empl_tuples_arr.append((employee.id_zam, employee_string))
    return empl_tuples_arr

def get_role_tuples():
    roles_tuples_arr = []
    for role in roles:
        if role == 'admin':
            role_string = "Administrátor"
        elif role == 'user':
            role_string = "Zaměstnanec"
        elif role == 'boss':
            role_string = "Vedoucí"
        roles_tuples_arr.append((role,role_string))
    return roles_tuples_arr