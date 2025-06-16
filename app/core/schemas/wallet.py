from typing import Optional
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class WalletRead(BaseModel):
    balance: Decimal = Field(json_schema_extra={'et': 0})


class WalletCreate(WalletRead):
    id: UUID
