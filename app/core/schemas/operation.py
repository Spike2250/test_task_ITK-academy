import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from .enums import OperationTypes
from utils.generics import TIMESTAMPAware


class OperationRequest(BaseModel):
    operation_type: str = OperationTypes
    amount: Decimal = Field(gt=0)


class OperationResult(BaseModel):
    message: str


class OperationSuccess(OperationResult):
    new_wallet_balance: Decimal


class OperationFailed(OperationResult):
    error_message: str


class OperationRead(OperationRequest):
    created_at: datetime.datetime
    id: UUID


