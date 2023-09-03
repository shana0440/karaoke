"""create_channels_table

Revision ID: 9ca9228053b7
Revises: 
Create Date: 2023-09-02 20:47:48.725690

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ca9228053b7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'channels',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('thumbnail_url', sa.String(), nullable=False),
        sa.Column('custom_url', sa.String(), nullable=False, unique=True),
        sa.Column('resource_id', sa.String(), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('channels')
