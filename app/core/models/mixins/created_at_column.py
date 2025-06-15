from datetime import datetime
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from app.utils import TIMESTAMPAware, now_utc


class CreatedAtColumnMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMPAware(timezone=True),
        index=True,
        nullable=False,
        default=now_utc,
    )
