"""init

Revision ID: 6b1a0ebfa443
Revises: 
Create Date: 2023-10-14 15:30:58.551396+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b1a0ebfa443'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('module_grade_structure',
    sa.Column('structure_id', sa.Integer(), nullable=False),
    sa.Column('module_id', sa.Integer(), nullable=False),
    sa.Column('structure_type', sa.Text(), nullable=False),
    sa.Column('structure_name', sa.Text(), nullable=True),
    sa.Column('weightage', sa.Numeric(), nullable=False),
    sa.ForeignKeyConstraint(['module_id'], ['modules.module_id'], ),
    sa.PrimaryKeyConstraint('structure_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('module_grade_structure')
    # ### end Alembic commands ###
