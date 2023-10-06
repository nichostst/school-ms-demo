"""init

Revision ID: 6633d2827a33
Revises: 927e1343fd19
Create Date: 2023-10-06 20:51:54.707181+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6633d2827a33'
down_revision: Union[str, None] = '927e1343fd19'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('modules_lecturers', sa.Column('lecturer_id', sa.Integer(), nullable=False))
    op.drop_constraint('modules_lecturers_coordinator_id_fkey', 'modules_lecturers', type_='foreignkey')
    op.create_foreign_key(None, 'modules_lecturers', 'users', ['lecturer_id'], ['user_id'])
    op.drop_column('modules_lecturers', 'coordinator_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('modules_lecturers', sa.Column('coordinator_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'modules_lecturers', type_='foreignkey')
    op.create_foreign_key('modules_lecturers_coordinator_id_fkey', 'modules_lecturers', 'users', ['coordinator_id'], ['user_id'])
    op.drop_column('modules_lecturers', 'lecturer_id')
    # ### end Alembic commands ###
