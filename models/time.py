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
    regular_hours: Mapped[str] = mapped_column(nullable=True,default=0) 
    regular_min: Mapped[str] = mapped_column(nullable=True,default=0)  

    over_hours: Mapped[str] = mapped_column(nullable=True,default=0)   
    over_min: Mapped[str] = mapped_column(nullable=True,default=0) 

    meal_hours: Mapped[str] = mapped_column(nullable=True,default=0)     
    meal_min: Mapped[str] = mapped_column(nullable=True,default=0)   

    sick_hours: Mapped[str] = mapped_column(nullable=True,default=0)
    sick_min: Mapped[str] = mapped_column(nullable=True,default=0)

    vacations_hours: Mapped[str] = mapped_column(nullable=True,default=0)  
    vacations_min: Mapped[str] = mapped_column(nullable=True,default=0)  


    sick_pay: Mapped[float] = mapped_column(nullable=True,default=0) 
    tips: Mapped[float] = mapped_column(nullable=True,default=0) 
    vacation_pay: Mapped[float] = mapped_column(nullable=True,default=0) 
    meal_time_pay: Mapped[float] = mapped_column(nullable=True,default=0)  
    overtime_pay: Mapped[float] = mapped_column(nullable=True,default=0)  
    regular_pay: Mapped[float] = mapped_column(nullable=True,default=0)  
    
    employer_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("employers.id"), nullable=True, index=True
    )
    
    employer = relationship("Employers", back_populates="time")
    payment = relationship("Payments", back_populates="time")
    

    

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
