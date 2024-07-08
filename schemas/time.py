from pydantic import BaseModel, ConfigDict, Field, validator, ValidationError
from schemas.payments import PaymentIDShema
from datetime import date, datetime
from typing import List

class TimeShema(BaseModel):
    regular_time: str 
    regular_amount: float = Field(ge=0, description="Debe ser un valor positivo")
    over_amount: float = Field(ge=0, description="Debe ser un valor positivo")
    meal_amount: float = Field(ge=0, description="Debe ser un valor positivo")
    over_time: str
    meal_time: str 
    holiday_time: str
    sick_time: str
    commissions: float = Field(ge=0, description="Debe ser un valor positivo")
    concessions: float = Field(ge=0, description="Debe ser un valor positivo")
    inability: float = Field(ge=0, description="Debe ser un valor positivo")
    medicare: float = Field(ge=0, description="Debe ser un valor positivo")
    secure_social: float = Field(ge=0, description="Debe ser un valor positivo")
    social_tips: float = Field(ge=0, description="Debe ser un valor positivo")
    tax_pr: float = Field(ge=0, description="Debe ser un valor positivo")
    choferil: float = Field(ge=0, description="Debe ser un valor positivo")
    vacations_hours: str  
    vacations_min: str  
    tips: float = Field(ge=0, description="Debe ser un valor positivo")
    payment: List[PaymentIDShema]
    memo: str = Field(max_length=150)
    model_config: ConfigDict(from_attributes=True)

    @validator('regular_time', 'over_time', 'meal_time', 'holiday_time', 'sick_time', 'vacations_hours', 'vacations_min')
    def check_time_format(cls, value):
        if not cls.valid_time_format(value):
            raise ValueError('El formato del tiempo es inválido')
        return value

    @validator('payment', pre=True)
    def check_payment_list(cls, value):
        if not isinstance(value, list) or not all(isinstance(item, PaymentIDShema) for item in value):
            raise ValueError('La lista de pagos es inválida')
        return value

    @staticmethod
    def valid_time_format(value: str) -> bool:
        try:
            datetime.strptime(value, '%H:%M')
            return True
        except ValueError:
            return False


class TimeIDShema(TimeShema):
    created_at: date
    id: int

class TimeIDShema2(TimeShema):
    id: int