"""add user table 

Revision ID: f3d979f821b9
Revises: 6b5a8b82366f
Create Date: 2024-07-02 16:34:36.265785

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3d979f821b9'
down_revision: Union[str, None] = '6b5a8b82366f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('users',
                    sa.Column('id',sa.Integer(), nullable=False),
                    sa.Column('email',sa.String(), nullable=False),
                    sa.Column('password',sa.String(), nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                              server_defult= sa.text('now()'),nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
