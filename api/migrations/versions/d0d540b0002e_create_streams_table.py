"""create_streams_table

Revision ID: d0d540b0002e
Revises: 9ca9228053b7
Create Date: 2023-09-02 20:47:51.349132

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd0d540b0002e'
down_revision: Union[str, None] = '9ca9228053b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'streams',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('video_id', sa.String(), nullable=False, unique=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('streamer_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('streams')
