import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from .enums import OperationTypes


class OperationRequest(BaseModel):
    operation_type: OperationTypes = Field(default=OperationTypes.DEPOSIT)
    amount: Decimal = Field(json_schema_extra={"gt": 0})


class OperationResult(BaseModel):
    message: str


class OperationSuccess(OperationResult):
    new_wallet_balance: Decimal


class OperationRead(OperationRequest):
    created_at: datetime.datetime
    id: UUID
