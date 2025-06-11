from fastapi import APIRouter

from core.config import settings

from .wallets import router as wallet_router

router = APIRouter(
    prefix=settings.api.v1.prefix
)
router.include_router(
    wallet_router,
    prefix=settings.api.v1.wallet,
)
