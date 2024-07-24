"""add last few columns to posts table

Revision ID: d6897eca5e3b
Revises: cdaf195d991c
Create Date: 2024-07-24 22:21:23.299499

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6897eca5e3b'
down_revision: Union[str, None] = 'cdaf195d991c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # op.add_column('posts',sa.Column('published',sa.Boolean(),nullable=False,server_default=sa.text('FALSE')))
    op.add_column('posts',
                  sa.Column('published',sa.Boolean(),nullable=False,server_default='TRUE'))
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
