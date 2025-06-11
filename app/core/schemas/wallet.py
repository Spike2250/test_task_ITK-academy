from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class WalletRead(BaseModel):
    balance: Decimal


class WalletCreate(WalletRead):
    id: UUID
