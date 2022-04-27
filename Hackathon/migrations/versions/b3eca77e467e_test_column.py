"""test column

Revision ID: b3eca77e467e
Revises: 60c7eaa36adf
Create Date: 2022-04-23 00:28:26.776696

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3eca77e467e'
down_revision = '60c7eaa36adf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('portfolio', schema=None) as batch_op:
        batch_op.add_column(sa.Column('test', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('portfolio', schema=None) as batch_op:
        batch_op.drop_column('test')

    # ### end Alembic commands ###
