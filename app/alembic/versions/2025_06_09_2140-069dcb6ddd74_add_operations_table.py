"""add operations table

Revision ID: 069dcb6ddd74
Revises: c9435a549639
Create Date: 2025-06-09 21:40:38.492202

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app import utils

# revision identifiers, used by Alembic.

revision: str = '069dcb6ddd74'
down_revision: Union[str, None] = 'c9435a549639'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'operations',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('wallet_id', sa.Uuid(), nullable=False),
        sa.Column(
            'operation_type',
            sa.Enum('DEPOSIT', 'WITHDRAW', name='operationtypes'),
            nullable=False
        ),
        sa.Column(
            'amount',
            sa.Numeric(precision=10, scale=2),
            nullable=False,
        ),
        sa.Column(
            'created_at',
            utils.generics.TIMESTAMPAware(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ['wallet_id'],
            ['wallets.id'],
            name=op.f('fk_operations_wallet_id_wallets'),
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_operations'))
    )
    op.create_index(
        op.f('ix_operations_created_at'),
        'operations',
        ['created_at'],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        op.f('ix_operations_created_at'),
        table_name='operations',
    )
    op.drop_table('operations')
