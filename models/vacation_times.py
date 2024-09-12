from typing import List
from sqlalchemy import TIMESTAMP, ForeignKey, Integer, String, Date, Boolean, func
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped

from database.config import Base

class VacationTimes(Base):
    __tablename__ = "vacation_times"


    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    employer_id: Mapped[int] = mapped_column(Integer, ForeignKey("employers.id"), nullable=True, index=True)
    vacation_hours: Mapped[int]
    sicks_hours: Mapped[int]
    year: Mapped[str]
    month: Mapped[str]