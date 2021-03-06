"""Create rectangle table

Revision ID: 9b8a24f39171
Revises: 13ccea44e73a
Create Date: 2020-12-18 14:58:45.777168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b8a24f39171'
down_revision = '13ccea44e73a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rectangles',
    sa.Column('rectangle_id', sa.Integer(), nullable=False),
    sa.Column('length', sa.Integer(), nullable=True),
    sa.Column('width', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('rectangle_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rectangles')
    # ### end Alembic commands ###
