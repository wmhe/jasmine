"""empty message

Revision ID: 3ed4e7d3ed5b
Revises: 0caaf5cfb87b
Create Date: 2025-01-02 16:23:34.786882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ed4e7d3ed5b'
down_revision = '0caaf5cfb87b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=False),
    sa.Column('start', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('event')
    # ### end Alembic commands ###