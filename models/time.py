from typing import List
from sqlalchemy import TIMESTAMP, ForeignKey, Integer, String,Date, Boolean, func
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from database.config import Base


class  Time(Base):
    __tablename__ = "employers_time"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    regular_time: Mapped[str] = mapped_column(String(50),nullable=True)    
    overtime: Mapped[str] = mapped_column(String(50),nullable=True)    
    meal_time: Mapped[str] = mapped_column(String(50),nullable=True)    
    sick_hours: Mapped[str] = mapped_column(String(50),nullable=True)    
    vacations_hours: Mapped[str] = mapped_column(String(50),nullable=True)    



    employer_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("employers.id"), nullable=True, index=True
    )
    
    employer = relationship("Employers", back_populates="time")
    

    

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
