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
    op.execute("alter table dokument drop foreign key dokument_ibfk_1;")
    op.drop_constraint('PRIMARY', 'vozidlo', type_='primary')
    op.execute("DELETE FROM vozidlo;")
    op.execute("ALTER TABLE vozidlo ADD id_voz int NOT NULL PRIMARY KEY AUTO_INCREMENT;")
    op.alter_column('dokument', 'spz', type_=sa.Integer, existing_type=sa.String(length=10), nullable=False, new_column_name='id_voz')
    op.create_foreign_key('fk_vozidlo_dokument', 'dokument', 'vozidlo', ['id_voz'], ['id_voz'])


def downgrade():
    op.drop_constraint('fk_vozidlo_dokument', 'dokument', type_='foreignkey')
    op.drop_column('vozidlo', 'id_voz')
    op.alter_column('dokument', 'id_voz', nullable=False, existing_type=sa.Integer, type_=sa.String(length=10), new_column_name='spz')
    op.create_primary_key('PRIMARY', 'vozidlo', ['spz'])
    op.create_foreign_key('dokument_ibfk_1', 'dokument', 'vozidlo', ['spz'], ['spz'])

