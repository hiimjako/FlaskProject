"""empty message

Revision ID: 07c18af6e3b6
Revises: fca1eb7ab8bf
Create Date: 2021-08-05 21:32:03.842508

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07c18af6e3b6'
down_revision = 'fca1eb7ab8bf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('files', 'filename',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('files', 'path',
               existing_type=sa.VARCHAR(length=512),
               nullable=True)
    op.alter_column('files', 'folder',
               existing_type=sa.VARCHAR(length=512),
               nullable=True)
    op.alter_column('files', 'size',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('files', 'size',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('files', 'folder',
               existing_type=sa.VARCHAR(length=512),
               nullable=False)
    op.alter_column('files', 'path',
               existing_type=sa.VARCHAR(length=512),
               nullable=False)
    op.alter_column('files', 'filename',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###
