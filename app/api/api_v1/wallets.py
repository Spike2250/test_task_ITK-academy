import uuid
from typing import Annotated, TYPE_CHECKING, Dict

from fastapi import APIRouter, Depends

from core.models import db_helper
from core.schemas.wallet import (
    WalletRead,
    WalletCreate,
)
from core.schemas.operation import OperationRequest

from .actions import (
    create_new_wallet,
    get_wallet_balance,
    create_new_transaction,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    tags=["Wallets"],
)


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


@router.put(
    "/{wallet_id}/operation",
    response_model=WalletRead,
)
async def create_transaction(
    wallet_id: uuid.UUID,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
    operation: OperationRequest = Depends(),
) -> Dict:
    return await create_new_transaction(
        wallet_id,
        operation,
        session,
    )
