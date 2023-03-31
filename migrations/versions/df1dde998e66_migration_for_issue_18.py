"""migration for issue 18

Revision ID: df1dde998e66
Revises: 4d3d27258039
Create Date: 2023-03-26 16:46:38.350449

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'df1dde998e66'
down_revision = '4d3d27258039'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('price',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('dish_price', sa.Float(), nullable=False),
    sa.Column('validity_start', sa.Date(), nullable=False),
    sa.Column('validity_end', sa.Date(), nullable=False),
    sa.Column('dish_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['dish_id'], ['dish.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('dish', 'price')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dish', sa.Column('price', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.drop_table('price')
    # ### end Alembic commands ###