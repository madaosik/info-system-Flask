"""Added service history table

Revision ID: 11d9759d3fad
Revises: f2ad5820f5aa
Create Date: 2018-12-16 15:57:35.933867

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11d9759d3fad'
down_revision = 'f2ad5820f5aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('service_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('car_id', sa.Integer(), nullable=False),
    sa.Column('short_desc', sa.String(length=25), nullable=False),
    sa.Column('long_desc', sa.String(length=100), nullable=True),
    sa.Column('mileage', sa.Integer(), nullable=True),
    sa.Column('mechanic', sa.String(length=25), nullable=True),
    sa.Column('receipt_no', sa.String(length=15), nullable=True),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('recorded_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('recorded_by', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['car_id'], ['vozidlo.id_voz'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['recorded_by'], ['zamestnanec.id_zam'], ondelete='NO ACTION'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('service_history')
    # ### end Alembic commands ###