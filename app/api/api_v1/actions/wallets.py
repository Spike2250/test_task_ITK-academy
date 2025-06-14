from typing import TYPE_CHECKING, Dict

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from core.models.wallet import Wallet
from core.models.operation import Operation
from core.schemas.wallet import WalletCreate, WalletRead
from core.schemas.operation import OperationSuccess, OperationFailed
from core.schemas.enums import OperationTypes


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from uuid import UUID
    from core.schemas.operation import OperationRequest


async def create_new_wallet(
    session: "AsyncSession"
) -> WalletCreate:
    new_wallet = Wallet()
    session.add(new_wallet)
    await session.flush()
    await session.commit()
    return WalletCreate.model_validate({
        "id": new_wallet.id,
        "balance": new_wallet.balance,
    })


async def get_wallet_balance(
    wallet_id: "UUID",
    session: "AsyncSession",
) -> WalletRead:
    wallet = await session.get(Wallet, wallet_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return WalletRead.model_validate({"balance": wallet.balance})


async def create_new_transaction(
    wallet_id: "UUID",
    operation: "OperationRequest",
    session: "AsyncSession",
) -> OperationSuccess | OperationFailed:
    try:
        new_operation = Operation(
            wallet_id=wallet_id,
            operation_type=operation.operation_type,
            amount=operation.amount,
        )
        session.add(new_operation)

        wallet = await get_wallet_balance(wallet_id, session)
        if operation.operation_type == OperationTypes.DEPOSIT:
            wallet.balance += operation.amount
        elif operation.operation_type == OperationTypes.WITHDRAW:
            wallet.balance -= operation.amount
        await session.flush()
        await session.commit()
        return OperationSuccess.model_validate({
            'message': 'The operation was successful!',
            'new_wallet_balance': wallet.balance,
        })
    except SQLAlchemyError as error:
        await session.rollback()
        return OperationFailed.model_validate({
            'message': 'The operation failed!!!',
            'error_message': error,
        })
