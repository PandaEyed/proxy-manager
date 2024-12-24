"""empty message

Revision ID: 7f467ab5d008
Revises: 5d00ab29f193
Create Date: 2024-12-19 14:13:30.701774

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f467ab5d008'
down_revision = '5d00ab29f193'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('scale_request',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('subject', sa.String(length=100), nullable=False, comment='主题'),
    sa.Column('description', sa.Text(), nullable=False, comment='描述需求'),
    sa.Column('request_type', sa.String(length=50), nullable=False, comment='单据类型'),
    sa.Column('status', sa.String(length=20), nullable=False, comment='状态'),
    sa.Column('created_at', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('scale_item',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nickname', sa.String(length=100), nullable=False, comment='FRPC 昵称'),
    sa.Column('progress', sa.Integer(), nullable=False, comment='扩展量'),
    sa.Column('frps_id', sa.Integer(), nullable=False, comment='关联 FRPS'),
    sa.Column('scale_request_id', sa.Integer(), nullable=False, comment='关联扩容单'),
    sa.ForeignKeyConstraint(['frps_id'], ['table_frps.id'], ),
    sa.ForeignKeyConstraint(['scale_request_id'], ['scale_request.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('scale_item')
    op.drop_table('scale_request')
    # ### end Alembic commands ###
