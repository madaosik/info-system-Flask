"""New primary key in vozidlo table - id instead of spz

Revision ID: ee542665fc4c
Revises: 2e3ba8b40eeb
Create Date: 2018-12-03 15:16:52.331110

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ee542665fc4c'
down_revision = '2e3ba8b40eeb'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('PRIMARY', 'vozidlo', type_='primary')
    op.execute("DELETE FROM vozidlo;")
    op.execute("ALTER TABLE vozidlo ADD id_voz int NOT NULL PRIMARY KEY AUTO_INCREMENT;")
    op.execute("INSERT INTO `vozidlo` VALUES ('5B4 1234','Mercedes','Atego',2008,110,100,4,'EURO III','2018-12-15 16:04:14','2018-12-15 16:04:14',1),('6B9 1234','Mercedes','Sprinter',2004,110,1100,4,'EURO IV','2018-12-15 16:08:06','2018-12-15 16:08:06',2),('1C9 5345','Mercedes','Vito',2003,80,900,3,'EURO III','2018-12-15 16:08:45','2018-12-15 16:08:45',3);")

def downgrade():
    op.execute("DELETE FROM vozidlo;")
    op.drop_column('vozidlo', 'id_voz')
    op.create_primary_key('PRIMARY', 'vozidlo', ['spz'])

