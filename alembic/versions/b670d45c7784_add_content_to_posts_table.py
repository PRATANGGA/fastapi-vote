"""add content to posts table

Revision ID: b670d45c7784
Revises: 6a2559f87062
Create Date: 2024-07-24 21:29:07.704645

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b670d45c7784'
down_revision: Union[str, None] = '6a2559f87062'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
