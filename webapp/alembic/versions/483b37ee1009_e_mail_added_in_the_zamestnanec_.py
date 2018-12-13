"""E-mail added in the Zamestnanec attributes

Revision ID: 483b37ee1009
Revises: cfb421ffa772
Create Date: 2018-10-28 09:45:27.351395

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '483b37ee1009'
down_revision = 'cfb421ffa772'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('zamestnanec', sa.Column('email', sa.String(30)))

def downgrade():
    op.drop_column('zamestnanec', 'email')
