from sqlalchemy import Column, Date, TIMESTAMP, String, Integer, func, ForeignKey, PrimaryKeyConstraint, Boolean
from flask_login import UserMixin
from webapp import db, login
from werkzeug.security import generate_password_hash, check_password_hash

class Zamestnanec(db.Model):
    __tablename__ = 'zamestnanec'

    id_zam = Column(Integer,primary_key=True)
    kr_jmeno = Column(String(20))
    prijmeni = Column(String(20))
    email = Column(String(30))
    dat_nar = Column(Date)
    trv_bydliste = Column(String(50))
    prech_bydliste = Column(String(50))
    telefon = Column(String(15))
    prac_sml = Column(String(15))
    akt_skol_id = Column(Integer)
    akt_prohlidka = Column(Integer)
    aktivni = Column(Integer)
    zalozen_cas = Column(TIMESTAMP, nullable=False, server_default=func.now())
    posl_aktual_cas = Column(TIMESTAMP, nullable=False, server_default=func.now(), server_onupdate=func.now())

    def __repr__(self):
        return "<Zamestanec(id='%d', jmeno='%s', prijmeni='%s')>" % (self.id_zam, self.kr_jmeno, self.prijmeni)

class Uzivatel(UserMixin, db.Model):
    __tablename__ = 'uzivatel'

    id = Column(Integer, autoincrement=True, primary_key=True)
    login = Column(String(30), nullable=False)
    password_hash = Column(String(128), nullable=False)
    email = Column(String(30), nullable=False)
    role = Column(String(10), server_default='user')
    poc_prihl = Column(Integer)
    posl_prihl = Column(TIMESTAMP)
    cas_posl_zmeny = Column(TIMESTAMP, server_default=func.now(), server_onupdate=func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_user_role(self):
        return self.role

@login.user_loader
def load_user(id):
    return Uzivatel.query.get(int(id))

class Skoleni_ridicu(db.Model):
    __tablename__= 'skoleni_ridicu'

    id_skol = Column(Integer, primary_key=True)
    id_zam = Column(Integer, ForeignKey("zamestnanec.id_zam", ondelete='CASCADE'), nullable=False)
    absolvovano_dne = Column(Date)
    platnost_do = Column(Date)
    posl_aktual = Column(TIMESTAMP, nullable=False, server_default=func.now(), server_onupdate=func.now())

class Lekarska_prohl(db.Model):
    __tablename__ = 'lekarska_prohl'

    id_prohl = Column(Integer, primary_key=True)
    id_zam = Column(Integer, ForeignKey("zamestnanec.id_zam", ondelete='CASCADE'), nullable=False)
    absolvovano_dne = Column(Date)
    platnost_do = Column(Date)
    posl_aktual = Column(TIMESTAMP, nullable=False, server_default=func.now(), server_onupdate=func.now())

class Pracovni_sml(db.Model):
    __tablename__ = 'pracovni_sml'

    id_sml = Column(Integer, primary_key=True)
    id_zam = Column(Integer, ForeignKey("zamestnanec.id_zam", ondelete='CASCADE'), nullable=False)
    typ_sml = Column(String(15)) # Dalsi tabulka "Typ smlouvy"?
    role_zam = Column(String(15)) # Dalsi tabulka "Role zam"?
    sjednana_dne = Column(Date)
    platnost_do = Column(Date)
    posl_aktual = Column(TIMESTAMP, nullable=False, server_default=func.now(), server_onupdate=func.now())

class Dovolena_zam(db.Model):
    __tablename__ = 'dovolena_zam'

    id_naroku = Column(Integer, primary_key=True)
    id_zam = Column(Integer, ForeignKey("zamestnanec.id_zam", ondelete='CASCADE'), nullable=False)
    rok = Column(Integer)
    narok = Column(Integer)
    vycerpano = Column(Integer)
    posl_aktual = Column(TIMESTAMP, nullable=False, server_default=func.now(), server_onupdate=func.now())

class Dovolena_zam_hist(db.Model):
    __tablename__ = 'dovolena_zam_hist'

    id_zaznamu = Column(Integer, primary_key=True)
    id_zam = Column(Integer, ForeignKey("zamestnanec.id_zam", ondelete='CASCADE'), nullable=False)
    rok = Column(Integer)
    od = Column(Date)
    do = Column(Date)
    celkem = Column(Integer)
    potvrzeni = Column(Boolean, default=False)

class Vozidlo(db.Model):
    __tablename__ = 'vozidlo'

    spz = Column(String(10),primary_key=True)
    znacka = Column(String(20))
    model = Column(String(20))
    rok_vyroby = Column(Integer)
    vykon = Column(Integer)
    nosnost = Column(Integer)
    pocet_naprav = Column(Integer)
    emisni_trida = Column(String(10))
    zalozeno_cas = Column(TIMESTAMP, nullable=False, server_default=func.now())
    posl_aktual_cas = Column(TIMESTAMP, nullable=False, server_default=func.now(), server_onupdate=func.now())


class Typ_dokumentu(db.Model):
    __tablename__ = 'typ_dokumentu'

    id_typu = Column(Integer, primary_key=True)
    popis_typu = String(20)

class Dokument(db.Model):
    __tablename__ = 'dokument'

    id_dokumentu = Column(Integer, primary_key=True)
    id_zam = Column(Integer, ForeignKey("zamestnanec.id_zam", ondelete='CASCADE'))
    id_voz = Column(String(10), ForeignKey("vozidlo.spz", ondelete='CASCADE'))
    typ_dokumentu = Column(Integer, ForeignKey("typ_dokumentu.id_typu", ondelete='CASCADE'))
    adresa_uloziste = Column(String(30),nullable=False)
    platnost_do = Column(Date)
    zalozen_cas = Column(TIMESTAMP, nullable=False, server_default=func.now())
    posl_editace = Column(TIMESTAMP, nullable=False, server_default=func.now(), server_onupdate=func.now())

class Sazba(db.Model):
    __tablename__ = 'sazba'

    id_sazby = Column(Integer,primary_key=True)
    popis_sazby = Column(String(30))
    vyse_sazby = Column(Integer)

class Cinnost(db.Model):
    __tablename__ = 'cinnost'

    id_cinnosti = Column(Integer, primary_key=True)
    typ_cinnosti = Column(String(30), nullable=False)
    odmena = Column(Integer,ForeignKey("sazba.id_sazby", ondelete='CASCADE'), nullable=False)

class Denni_evidence(db.Model):
    __tablename__ = 'denni_evidence'
    __table_args__ = (PrimaryKeyConstraint('id_cinnosti','id_zam'),)

    id_cinnosti = Column(Integer, ForeignKey("cinnost.id_cinnosti", ondelete='CASCADE'), nullable=False)
    id_zam = Column(Integer, ForeignKey("zamestnanec.id_zam", ondelete='CASCADE'), nullable=False)
    den_uskut = Column(Date)
    cas_uloz = Column(TIMESTAMP, nullable=False, server_default=func.now())
    cas_zmeny = Column(TIMESTAMP, nullable=False, server_default=func.now(), server_onupdate=func.now())