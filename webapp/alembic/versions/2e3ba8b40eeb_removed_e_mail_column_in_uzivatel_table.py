"""Removed e-mail column in uzivatel table

Revision ID: 2e3ba8b40eeb
Revises: 6b60e92cc7a0
Create Date: 2018-12-03 14:56:49.739348

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2e3ba8b40eeb'
down_revision = '6b60e92cc7a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('uzivatel', 'email')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('uzivatel', sa.Column('email', mysql.VARCHAR(length=30), nullable=False))
    # ### end Alembic commands ###