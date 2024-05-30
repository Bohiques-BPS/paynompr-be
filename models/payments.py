from typing import List
from sqlalchemy import TIMESTAMP, ForeignKey, Integer, String,Date, Boolean, func
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from database.config import Base


class  Payments(Base):
    __tablename__ = "taxes_time"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    name: Mapped[str] = mapped_column(String(50),nullable=False,)    
    amount: Mapped[float] = mapped_column(nullable=True,default=0)  
    value: Mapped[float] = mapped_column(nullable=True,default=0)  
    
    requiered: Mapped[float] = mapped_column(nullable=True,default=0)  
    type_taxe: Mapped[float] = mapped_column(nullable=True,default=0)  
    type_amount: Mapped[float] = mapped_column(nullable=True,default=0)  

    time_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("employers_time.id"), nullable=True, index=True
    )
    

    time = relationship("Time", back_populates="payment")
    

    

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=True)
    deleted_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    update_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True,
        onupdate=func.now(),
    )
