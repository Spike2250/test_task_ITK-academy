from decimal import Decimal
import uuid

from sqlalchemy import (
    Numeric,
    Enum,
    ForeignKey,
)
from sqlalchemy.orm import (
    mapped_column,
    Mapped,
)

from .base import Base
from .mixins import (
    UuidIdPkMixin,
    CreatedAtColumnMixin,
)
from core.schemas.enums import OperationTypes


class Operation(UuidIdPkMixin, CreatedAtColumnMixin, Base):
    wallet_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('wallets.id'),
        nullable=False,
    )
    operation_type: Mapped[str] = mapped_column(
        Enum(OperationTypes),
        nullable=False,
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        default=Decimal("0.00")
    )
