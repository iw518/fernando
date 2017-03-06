"""empty message

Revision ID: 1b61dc0c97a6
Revises: None
Create Date: 2016-12-19 18:11:10.778324

"""

# revision identifiers, used by Alembic.
revision = '1b61dc0c97a6'
down_revision = None

import sqlalchemy as sa
from alembic import op


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profiles', sa.Column('contract_sum', sa.Integer(), nullable=True))
    op.add_column('profiles', sa.Column('income_sum', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('profiles', 'income_sum')
    op.drop_column('profiles', 'contract_sum')
    ### end Alembic commands ###
