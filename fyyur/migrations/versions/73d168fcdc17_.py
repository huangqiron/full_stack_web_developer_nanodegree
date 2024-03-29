"""empty message

Revision ID: 73d168fcdc17
Revises: 11f1a5d21e34
Create Date: 2020-08-25 20:01:00.309178

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73d168fcdc17'
down_revision = '11f1a5d21e34'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('website', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artist', 'website')
    # ### end Alembic commands ###
