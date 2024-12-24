"""empty message

Revision ID: 6fcd5fb532d2
Revises: 7f467ab5d008
Create Date: 2024-12-22 14:40:46.895066

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6fcd5fb532d2'
down_revision = '7f467ab5d008'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('table_frpc', schema=None) as batch_op:
        batch_op.alter_column('user',
               existing_type=mysql.VARCHAR(length=100),
               comment='使用方',
               existing_comment='用房',
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('table_frpc', schema=None) as batch_op:
        batch_op.alter_column('user',
               existing_type=mysql.VARCHAR(length=100),
               comment='用房',
               existing_comment='使用方',
               existing_nullable=True)

    # ### end Alembic commands ###
