"""create post table

Revision ID: 07ec1b8774cf
Revises: 
Create Date: 2024-07-02 16:15:44.881724

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07ec1b8774cf'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('posts', sa.Column('id',sa.Integer(), nullable=False, primary_key=True), 
                    sa.column('title',sa.String()))
    pass


def downgrade():
    op.drop_table('posts')
    pass
