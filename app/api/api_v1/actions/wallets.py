from typing import TYPE_CHECKING

from fastapi import HTTPException

from core.models.wallet import Wallet
from core.schemas.wallet import WalletCreate, WalletRead


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from uuid import UUID


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
    return wallet
