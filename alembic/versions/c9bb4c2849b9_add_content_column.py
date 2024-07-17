"""add content column

Revision ID: c9bb4c2849b9
Revises: 1c662ebf1431
Create Date: 2024-07-16 21:23:57.794346

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c9bb4c2849b9'
down_revision: Union[str, None] = '1c662ebf1431'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
