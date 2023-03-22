"""empty message

Revision ID: 3846339b9375
Revises: 268b3b8aedda
Create Date: 2023-03-22 17:24:24.327836

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3846339b9375'
down_revision = '268b3b8aedda'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('assignments', schema=None) as batch_op:
        batch_op.drop_column('due_date')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('assignments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('due_date', postgresql.TIME(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
