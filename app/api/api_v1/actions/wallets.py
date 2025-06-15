from typing import TYPE_CHECKING
from datetime import datetime

from fastapi import HTTPException

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from core.models.wallet import Wallet
from core.models.operation import Operation
from core.schemas.wallet import WalletCreate, WalletRead
from core.schemas.operation import OperationSuccess, OperationFailed, OperationRead
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
        wallet = await session.get(
            Wallet,
            wallet_id,
            with_for_update=True,  # важно(!) для контроля изменений
        )
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")

        if operation.operation_type == OperationTypes.DEPOSIT:
            wallet.balance += operation.amount
        elif operation.operation_type == OperationTypes.WITHDRAW:
            if wallet.balance < operation.amount:
                raise HTTPException(
                    status_code=400,
                    detail="Insufficient funds"
                )
            wallet.balance -= operation.amount
        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid operation type"
            )

        session.add(
            Operation(
                wallet_id=wallet_id,
                operation_type=operation.operation_type,
                amount=operation.amount,
            )
        )
        await session.flush()
        await session.refresh(wallet)

        return OperationSuccess.model_validate({
            'message': 'The operation was successful!',
            'new_wallet_balance': wallet.balance,
        })
    except SQLAlchemyError | HTTPException as error:
        await session.rollback()
        return OperationFailed.model_validate({
            'message': 'The operation failed!!!',
            'error_message': error,
        })


async def __get_operation(
    operation_id: "UUID",
    session: "AsyncSession",
) -> OperationRead:

    operation = await session.get(Operation, operation_id)
    if not operation:
        raise HTTPException(status_code=404, detail="Operation not found")
    return OperationRead.model_validate({
        'operation_type': operation.operation_type,
        'amount': operation.amount,
        'created_at': operation.created_at,
        'id': operation.id,
    })


async def get_operation(
    wallet_id: "UUID",
    operation_id: "UUID",
    session: "AsyncSession",
) -> OperationRead:
    if await get_wallet_balance(wallet_id, session):
        return await __get_operation(operation_id, session)


async def __get_operations(
    wallet_id: "UUID",
    session: "AsyncSession",
    limit: int = 25,
) -> list[OperationRead]:
    query = select(Operation)\
                .filter(Operation.wallet_id == wallet_id)\
                .order_by(Operation.created_at.desc())\
                .limit(limit)
    result = await session.execute(query)
    operations = result.scalars().all()
    return [
        OperationRead(
            operation_type=opr.operation_type,
            amount=opr.amount,
            created_at=opr.created_at,
            id=opr.id,
        ) for opr in operations
    ]


async def get_operations_history(
    wallet_id: "UUID",
    session: "AsyncSession",
    limit: int = 25,
) -> list[OperationRead]:
    if await get_wallet_balance(wallet_id, session):
        return await __get_operations(wallet_id, session, limit)
