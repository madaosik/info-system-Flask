# -*- coding: utf-8 -*-

from webapp.core.models import *
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


def edit_user_from_form(id,form_data):
    user = get_user_by_attr(id=id)

    try:
        user.role = form_data['role']
    except KeyError:
        pass

    if len(form_data['password']) > 0:
        user.set_password(form_data['password'])
    user.login = form_data['login']
    session.commit()

def create_user(**kwargs):
    if 'login' in kwargs:
        login = kwargs['login']
    else:
        login = "xuser"
        if not is_login_valid(login):
            for i in range(1, 99):
                login = login + str(i)
                if is_login_valid(login):
                    break

    user = Uzivatel(login=login,id_zam=kwargs['employee_id'])

    if 'password' in kwargs:
        user.set_password(kwargs['password'])
    else:
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

def get_first_car_id():
    pass

def fetch_service_history(car_id):
    pass


def fetch_all_pending_approvals():
    return Activity.query.filter_by(approved=False).first()



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

def fetch_unseen_zam_vacation(id):
    return Dovolena_zam_hist.query.filter_by(id_zam=id, seen_by_zam=False).first()


def mark_seen_zam_vacation(id):
    q = Dovolena_zam_hist.query.filter_by(id_zam=id, seen_by_zam=False)
    for a in q:
        a.seen_by_zam = True
    session.commit()


#Activity functions

def approve_act(id):
    q = Activity.query.get(id)
    q.approved = True
    q.seen = True
    session.commit()


def decline_act(id):
    q = Activity.query.get(id)
    q.approved = False
    q.seen = True
    session.commit()


def delete_act(id):
    session.query(Activity).filter_by(id_activity=id).delete()
    session.commit()


def edit_act_payoff(id,payoff):
    q = Activity.query.get(id)
    q.payoff = payoff
    session.commit()


def fetch_activity_by_id_zam(id):
    return Activity.query.filter_by(id_zam=id)


def fetch_activity_by_id_act(id):
    return Activity.query.filter_by(id_activity=id).first()


def update_activity_by_id_act(id,act):
    q =Activity.query.filter_by(id_activity=id).first()
    q = act
    session.commit()



# Employee functions

def delete_employee(id):
    session.query(Zamestnanec).filter_by(id_zam=id).delete()
    session.commit()

def fetch_employee_by_id(id):
    return Zamestnanec.query.filter_by(id_zam=id).first()

def get_empl_from_user(user_id):
    user = session.query(Uzivatel).filter_by(id=user_id).first()
    return session.query(Zamestnanec).filter_by(id_zam=user.id_zam).first()

# User functions

def delete_user(id):
    session.query(Uzivatel).filter_by(id=id).delete()
    session.commit()

def fetch_user_tuples():
    return (session.query(Uzivatel, Zamestnanec).filter(Uzivatel.id_zam == Zamestnanec.id_zam).all())


def get_employee_tuples():
    employees = Zamestnanec.query.all()
    empl_tuples_arr = []
    for employee in employees:
        if Uzivatel.query.filter_by(id_zam=employee.id_zam).first() is None:
            employee_string = "%s %s" % (employee.kr_jmeno, employee.prijmeni)
            empl_tuples_arr.append((employee.id_zam, employee_string))
    return empl_tuples_arr




