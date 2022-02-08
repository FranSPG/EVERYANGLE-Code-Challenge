"""empty message

Revision ID: f6831c162b8d
Revises: 2e23425a07e5
Create Date: 2022-02-08 00:44:55.846776

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6831c162b8d'
down_revision = '2e23425a07e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('media', 'category_name',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.Text(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('media', 'category_name',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=50),
               existing_nullable=True)
    # ### end Alembic commands ###
