"""add wallets table

Revision ID: c9435a549639
Revises:
Create Date: 2025-06-09 18:08:29.794209

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c9435a549639'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'wallets',
        sa.Column(
            'id',
            sa.Uuid(),
            nullable=False,
        ),
        sa.Column(
            'balance',
            sa.Numeric(precision=10, scale=2),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_wallets'))
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('wallets')
