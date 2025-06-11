from typing import TYPE_CHECKING

from core.models.wallet import Wallet
from core.schemas.wallet import WalletCreate, WalletRead


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


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
