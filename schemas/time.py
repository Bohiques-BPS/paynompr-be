from pydantic import BaseModel, ConfigDict
from schemas.payments import PaymentIDShema
from datetime import date

class TimeShema(BaseModel):
    regular_time : int
    overtime : int
    meal_time : int
    sick_hours : int
    vacations_hours :  int
    sick_pay: int
    regular_pay: float
    vacation_pay:float
    meal_time_pay: float
    overtime_pay:float 
   
    payments: list[PaymentIDShema]
     

    model_config : ConfigDict(from_attributes=True)


class TimeIDShema(TimeShema):
    created_at : date
    id: int
   

