from pydantic import BaseModel, ConfigDict
from schemas.payments import PaymentIDShema
from datetime import date

class TimeShema(BaseModel):
    regular_time : str
    overtime : str
    meal_time : str
    sick_hours : str
    vacations_hours :  str
    sick_pay: float
    regular_pay: float
    vacation_pay:float
    meal_time_pay: float
    overtime_pay:float 
    tips: float
    payments: list[PaymentIDShema]
     

    model_config : ConfigDict(from_attributes=True)


class TimeIDShema(TimeShema):
    created_at : date
    id: int
   

