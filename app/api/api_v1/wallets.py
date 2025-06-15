import uuid
from typing import Annotated, TYPE_CHECKING, Dict

from fastapi import APIRouter, Depends

from core.models import db_helper
from core.schemas.wallet import (
    WalletRead,
    WalletCreate,
)
from core.schemas.operation import (
    OperationRequest,
    OperationSuccess,
    OperationFailed,
    OperationRead,
)

from .actions import (
    create_new_wallet,
    get_wallet_balance,
    create_new_transaction,
    get_operation,
    get_operations_history,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    tags=["Wallets"],
)


@router.post(
    "",
    response_model=WalletCreate,
)
async def create_wallet(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    return await create_new_wallet(session)


@router.get(
    "/{wallet_id}",
    response_model=WalletRead,
)
async def get_balance(
    wallet_id: uuid.UUID,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    return await get_wallet_balance(wallet_id, session)


@router.put(
    "/{wallet_id}/operation",
    response_model=OperationSuccess | OperationFailed,
)
async def create_transaction(
    wallet_id: uuid.UUID,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
    operation: OperationRequest = Depends(),
):
    return await create_new_transaction(
        wallet_id,
        operation,
        session,
    )


@router.get(
    "/{wallet_id}/operation/{operation_id}",
    response_model=OperationRead,
)
async def get_operation_from_id(
    wallet_id: uuid.UUID,
    operation_id: uuid.UUID,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    return await get_operation(wallet_id, operation_id, session)


@router.get(
    "/{wallet_id}/operations",
    response_model=list[OperationRead],
)
async def get_operations(
    wallet_id: uuid.UUID,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
    limit: int = 25,
):
    return await get_operations_history(wallet_id, session, limit)
