from app.core.schemas.operation import (
    OperationRequest,
    OperationTypes,
)
from uuid import uuid4
from decimal import Decimal


PREFIX = "/api/v1"
TEST_AMOUNT = Decimal(100)
TEST_DEPOSIT = OperationRequest(
    operation_type=OperationTypes.DEPOSIT,
    amount=TEST_AMOUNT
)
TEST_VALID_WITHDRAW = OperationRequest(
    operation_type=OperationTypes.WITHDRAW,
    amount=TEST_AMOUNT // 2
)
TEST_OVERDRAFT_WITHDRAW = OperationRequest(
    operation_type=OperationTypes.WITHDRAW,
    amount=TEST_AMOUNT * 2
)
INVALID_UUID = uuid4()
