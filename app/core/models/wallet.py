from decimal import Decimal

from sqlalchemy import Numeric
from sqlalchemy.orm import (
    mapped_column,
    Mapped,
)

from .base import Base
from .mixins import UuidIdPkMixin


class Wallet(UuidIdPkMixin, Base):
    balance: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        default=Decimal("0.00"),
    )
