"""add user table

Revision ID: b7690780899e
Revises: b670d45c7784
Create Date: 2024-07-24 21:37:44.908594

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7690780899e'
down_revision: Union[str, None] = 'b670d45c7784'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(),nullable=False),sa.Column('email',sa.String(),nullable=False),sa.Column('password',sa.String(),nullable=False),sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')),sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),)
    pass


def downgrade() -> None:
    op.drop_column('users')
    pass
