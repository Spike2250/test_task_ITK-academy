import uuid
from typing import Annotated, TYPE_CHECKING

from fastapi import APIRouter, Depends

from core.models import db_helper
from core.schemas.wallet import (
    WalletRead,
    WalletCreate,
)

from .actions import (
    create_new_wallet,
    get_wallet_balance,
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


# @router.put(
#     "/{wallet_id}/operation",
#     response_model=WalletRead,
# )
# async def
