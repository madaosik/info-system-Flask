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

def downgrade():
    op.execute("DELETE FROM vozidlo;")
    op.drop_column('vozidlo', 'id_voz')
    op.create_primary_key('PRIMARY', 'vozidlo', ['spz'])

