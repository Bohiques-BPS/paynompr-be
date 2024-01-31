from typing import List
from sqlalchemy import TIMESTAMP, ForeignKey, Integer, String, Boolean, func
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from database.config import Base


class  Employers(Base):
    __tablename__ = "employers"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    last_name: Mapped[str] = mapped_column(String(50),nullable=False)    
    mother_last_name: Mapped[str] = mapped_column(String(50),nullable=False)    
    first_name: Mapped[str] = mapped_column(String(50),nullable=False)    
    middle_name: Mapped[str] = mapped_column(String(50),nullable=False)  
    company_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("companies.id"), nullable=False, index=True
    )  
    
    employee_type: Mapped[str] = mapped_column(String(50),nullable=False)    
    social_security_number: Mapped[str] = mapped_column(String(50),nullable=False)    
    marital_status: Mapped[str] = mapped_column(String(50),nullable=False)    
    address: Mapped[str] = mapped_column(String(50),nullable=False)    
    address_state: Mapped[str] = mapped_column(String(50),nullable=False)    
    address_country: Mapped[str] = mapped_column(String(50),nullable=False)    
    address_number: Mapped[str] = mapped_column(String(50),nullable=False)    
    phone_number: Mapped[str] = mapped_column(String(50),nullable=False)    
    smartphone_number: Mapped[str] = mapped_column(String(50),nullable=False)    

    

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=False), nullable=True
    )
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=False), server_default=func.now()
    )
    update_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=False),
        nullable=True,
        onupdate=func.now(),
    )
