"""add content collumn to post table

Revision ID: 6b5a8b82366f
Revises: 07ec1b8774cf
Create Date: 2024-07-02 16:28:03.616959

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b5a8b82366f'
down_revision: Union[str, None] = '07ec1b8774cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')

    pass
