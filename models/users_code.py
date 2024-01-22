from sqlalchemy import TIMESTAMP, ForeignKey, Integer, Boolean, func
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped

from database.config import Base


class UserCode(Base):
    __tablename__ = "users_code"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    code_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("codes.id"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
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
