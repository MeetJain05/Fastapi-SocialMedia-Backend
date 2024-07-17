"""create posts table

Revision ID: 1c662ebf1431
Revises: 
Create Date: 2024-07-14 23:23:48.858413

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c662ebf1431'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.INTEGER(),nullable=False, primary_key=True),
     sa.Column('title', sa.String,nullable=False))
    
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
