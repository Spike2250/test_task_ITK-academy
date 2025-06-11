from decimal import Decimal

from pydantic import BaseModel, Field

from .enums import OperationTypes


class OperationRequest(BaseModel):
    operation_type: str = OperationTypes
    amount: Decimal = Field(gt=0)
