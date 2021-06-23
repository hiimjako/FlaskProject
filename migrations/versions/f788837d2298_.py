"""empty message

Revision ID: f788837d2298
Revises: c7d5bea8e7e6
Create Date: 2021-06-23 18:52:38.919935

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f788837d2298'
down_revision = 'c7d5bea8e7e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('files', sa.Column('size', sa.Integer()))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('files', 'size')
    # ### end Alembic commands ###
