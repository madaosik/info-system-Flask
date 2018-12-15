"""Added id_zam foreign key to Uzivatel

Revision ID: 6b60e92cc7a0
Revises: 94351efaa16e
Create Date: 2018-12-03 09:51:33.964961

"""
from alembic import op
import sqlalchemy as sa
from webapp.core import models

# revision identifiers, used by Alembic.
revision = '6b60e92cc7a0'
down_revision = '94351efaa16e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("DELETE FROM %s;" % 'uzivatel')
    op.add_column('uzivatel', sa.Column('id_zam', sa.Integer(), nullable=False))
    op.create_foreign_key('uzivatel_zamestnanec', 'uzivatel', 'zamestnanec', ['id_zam'], ['id_zam'], ondelete='CASCADE')
    # ### end Alembic commands ###
    op.execute("DELETE FROM zamestnanec;")
    op.execute("INSERT INTO `zamestnanec` VALUES (2,'Jana','Horáčková','1991-07-19','Nového 20, 616 00, Brno','','58','2',NULL,NULL,1,'2018-10-27 17:29:08','2018-10-27 17:29:08','e.e@gmail.com'),(43,'Kryštof','Novotný','2018-12-06','','','','',NULL,NULL,1,'2018-12-12 07:24:51','2018-12-12 07:24:51','e@e.cz'),(44,'Petr','Novák','2018-12-13','Křtiny 25, 660 00 Křtiny','','+4206071135467','',NULL,NULL,1,'2018-12-12 07:30:04','2018-12-12 07:30:04','a@d.cz'),(46,'Křivoklát','Smetana','2018-11-28','','','','',NULL,NULL,1,'2018-12-13 08:55:59','2018-12-13 08:55:59','d@s.cz'),(49,'Leontýna','Nová','2018-12-21','','','99999999','',NULL,NULL,1,'2018-12-13 09:12:34','2018-12-13 09:12:34','s@s.cz'),(50,'Adam','Sova','2018-12-06','sdasdasd','','','',NULL,NULL,1,'2018-12-15 12:49:03','2018-12-15 12:49:03','a@a.cz');")

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uzivatel_zamestnanec', 'uzivatel', type_='foreignkey')
    op.drop_column('uzivatel', 'id_zam')
    # ### end Alembic commands ###
