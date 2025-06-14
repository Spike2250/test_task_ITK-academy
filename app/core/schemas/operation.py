from decimal import Decimal

from pydantic import BaseModel, Field

from .enums import OperationTypes


class OperationRequest(BaseModel):
    operation_type: str = OperationTypes
    amount: Decimal = Field(gt=0)


class OperationResult(BaseModel):
    message: str


class OperationSuccess(OperationResult):
    new_wallet_balance: Decimal


class OperationFailed(OperationResult):
    error_message: str
