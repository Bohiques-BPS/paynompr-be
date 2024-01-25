from sqlalchemy import TIMESTAMP, Integer, String, Boolean, func
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped

from database.config import Base


class Code(Base):
    __tablename__ = "codes"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    email: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    owner: Mapped[str] = mapped_column(String(50), nullable=False)
    amount: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1, server_default="1"
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=False), nullable=True
    )
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=False), server_default=func.now(), nullable=False
    )
    update_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=False),
        nullable=True,
        onupdate=func.now(),
    )
