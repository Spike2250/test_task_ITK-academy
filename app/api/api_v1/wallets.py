import uuid
from typing import Annotated, TYPE_CHECKING

from fastapi import APIRouter, Depends, HTTPException

from core.models import db_helper, Wallet
from core.schemas.wallet import (
    WalletRead,
    WalletCreate,
)
from utils import GUID

from .actions import create_new_wallet

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    tags=["Wallets"],
)


@router.get(
    "/{wallet_id}",
    response_model=WalletRead,
)
async def get_wallet_balance(
    wallet_id: uuid.UUID,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    wallet = await session.get(Wallet, wallet_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet


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
    # return await create_new_wallet(session)
    new_wallet = Wallet()
    session.add(new_wallet)
    await session.flush()
    await session.commit()
    return WalletCreate.model_validate({
        "id": new_wallet.id,
        "balance": new_wallet.balance,
    })


# @router.put(
#     "/{wallet_id}/operation",
#     response_model=WalletRead,
# )
# async def
