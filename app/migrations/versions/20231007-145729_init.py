"""init

Revision ID: 357bbf4c0bb5
Revises: 1d8b70fe174e
Create Date: 2023-10-07 14:57:29.498622+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '357bbf4c0bb5'
down_revision: Union[str, None] = '1d8b70fe174e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('modules_coordinators', 'assigned_at')
    op.drop_column('modules_lecturers', 'assigned_at')
    op.add_column('modules_students', sa.Column('student_id', sa.Integer(), nullable=False))
    op.alter_column('modules_students', 'term_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint('modules_students_coordinator_id_fkey', 'modules_students', type_='foreignkey')
    op.create_foreign_key(None, 'modules_students', 'users', ['student_id'], ['user_id'])
    op.drop_column('modules_students', 'coordinator_id')
    op.drop_column('modules_students', 'assigned_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('modules_students', sa.Column('assigned_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False))
    op.add_column('modules_students', sa.Column('coordinator_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'modules_students', type_='foreignkey')
    op.create_foreign_key('modules_students_coordinator_id_fkey', 'modules_students', 'users', ['coordinator_id'], ['user_id'])
    op.alter_column('modules_students', 'term_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('modules_students', 'student_id')
    op.add_column('modules_lecturers', sa.Column('assigned_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False))
    op.add_column('modules_coordinators', sa.Column('assigned_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False))
    # ### end Alembic commands ###