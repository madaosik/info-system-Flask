from sqlalchemy import Column, Date, TIMESTAMP, String, Integer, func, ForeignKey, PrimaryKeyConstraint, Boolean
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from webapp.core.db_connector import Base

class Zamestnanec(Base):
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
        return "<Zamestnanec(id='%d', jmeno='%s', prijmeni='%s')>" % (self.id_zam, self.kr_jmeno, self.prijmeni)

class Uzivatel(UserMixin, Base):
    __tablename__ = 'uzivatel'

    id = Column(Integer, autoincrement=True, primary_key=True)
    login = Column(String(30), nullable=False)
    password_hash = Column(String(128), nullable=False)
    role = Column(String(10), server_default='user')
    id_zam = Column(Integer, ForeignKey("zamestnanec.id_zam", ondelete='CASCADE'), nullable=False)
    poc_prihl = Column(Integer)
    posl_prihl = Column(TIMESTAMP)
    cas_posl_zmeny = Column(TIMESTAMP, server_default=func.now(), server_onupdate=func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    #def get_user_role(self):
        #return self.role
    def is_employee(self):
        return True if self.role == 'user' else False

    def is_boss(self):
        return True if self.role == 'boss' else False

    def is_admin(self):
        return True if self.role == 'admin' else False


class Skoleni_ridicu(Base):
    __tablename__= 'skoleni_ridicu'

    id_skol = Column(Integer, primary_key=True)
    id_zam = Column(Integer, ForeignKey("zamestnanec.id_zam", ondelete='CASCADE'), nullable=False)
    absolvovano_dne = Column(Date)
    platnost_do = Column(Date)
    posl_aktual = Column(TIMESTAMP, nullable=False, server_default=func.now(), server_onupdate=func.now())

class Lekarska_prohl(Base):
    __tablename__ = 'lekarska_prohl'

    id_prohl = Column(Integer, primary_key=True)
    id_zam = Column(Integer, ForeignKey("zamestnanec.id_zam", ondelete='CASCADE'), nullable=False)
    absolvovano_dne = Column(Date)
    platnost_do = Column(Date)
    posl_aktual = Column(TIMESTAMP, nullable=False, server_default=func.now(), server_onupdate=func.now())

class Pracovni_sml(Base):
    __tablename__ = 'pracovni_sml'

    id_sml = Column(Integer, primary_key=True)
    id_zam = Column(Integer, ForeignKey("zamestnanec.id_zam", ondelete='CASCADE'), nullable=False)
    typ_sml = Column(String(15)) # Dalsi tabulka "Typ smlouvy"?
    role_zam = Column(String(15)) # Dalsi tabulka "Role zam"?
    sjednana_dne = Column(Date)
    platnost_do = Column(Date)
    posl_aktual = Column(TIMESTAMP, nullable=False, server_default=func.now(), server_onupdate=func.now())

class Dovolena_zam(Base):
    __tablename__ = 'dovolena_zam'

    id_naroku = Column(Integer, primary_key=True)
    id_zam = Column(Integer, ForeignKey("zamestnanec.id_zam", ondelete='CASCADE'), nullable=False)
    rok = Column(Integer)
    narok = Column(Integer)
    vycerpano = Column(Integer)
    posl_aktual = Column(TIMESTAMP, nullable=False, server_default=func.now(), server_onupdate=func.now())

class Dovolena_zam_hist(Base):
    __tablename__ = 'dovolena_zam_hist'

    id_zaznamu = Column(Integer, primary_key=True)
    id_zam = Column(Integer, ForeignKey("zamestnanec.id_zam", ondelete='CASCADE'), nullable=False)
    rok = Column(Integer)
    od = Column(Date)
    do = Column(Date)
    celkem = Column(Integer)
    potvrzeni = Column(Boolean, default=False)
    #seen = Column(Boolean, default=False)

class Vozidlo(Base):
    __tablename__ = 'vozidlo'

    id_voz = Column(Integer, primary_key=True)
    spz = Column(String(10))
    znacka = Column(String(20))
    model = Column(String(20))
    rok_vyroby = Column(Integer)
    vykon = Column(Integer)
    nosnost = Column(Integer)
    pocet_naprav = Column(Integer)
    emisni_trida = Column(String(10))
    zalozeno_cas = Column(TIMESTAMP, nullable=False, server_default=func.now())
    posl_aktual_cas = Column(TIMESTAMP, nullable=False, server_default=func.now(), server_onupdate=func.now())


class Typ_dokumentu(Base):
    __tablename__ = 'typ_dokumentu'

    id_typu = Column(Integer, primary_key=True)
    popis_typu = String(20)

class Dokument(Base):
    __tablename__ = 'dokument'

    id_dokumentu = Column(Integer, primary_key=True)
    id_zam = Column(Integer, ForeignKey("zamestnanec.id_zam", ondelete='CASCADE'))
    id_voz = Column(String(10), ForeignKey("vozidlo.spz", ondelete='CASCADE'))
    typ_dokumentu = Column(Integer, ForeignKey("typ_dokumentu.id_typu", ondelete='CASCADE'))
    adresa_uloziste = Column(String(30),nullable=False)
    platnost_do = Column(Date)
    zalozen_cas = Column(TIMESTAMP, nullable=False, server_default=func.now())
    posl_editace = Column(TIMESTAMP, nullable=False, server_default=func.now(), server_onupdate=func.now())

class Sazba(Base):
    __tablename__ = 'sazba'

    id_sazby = Column(Integer,primary_key=True)
    popis_sazby = Column(String(30))
    vyse_sazby = Column(Integer)

class Cinnost(Base):
    __tablename__ = 'cinnost'

    id_cinnosti = Column(Integer, primary_key=True)
    typ_cinnosti = Column(String(30), nullable=False)
    odmena = Column(Integer,ForeignKey("sazba.id_sazby", ondelete='CASCADE'), nullable=False)

class Denni_evidence(Base):
    __tablename__ = 'denni_evidence'
    __table_args__ = (PrimaryKeyConstraint('id_cinnosti','id_zam'),)

    id_cinnosti = Column(Integer, ForeignKey("cinnost.id_cinnosti", ondelete='CASCADE'), nullable=False)
    id_zam = Column(Integer, ForeignKey("zamestnanec.id_zam", ondelete='CASCADE'), nullable=False)
    den_uskut = Column(Date)
    cas_uloz = Column(TIMESTAMP, nullable=False, server_default=func.now())
    cas_zmeny = Column(TIMESTAMP, nullable=False, server_default=func.now(), server_onupdate=func.now())