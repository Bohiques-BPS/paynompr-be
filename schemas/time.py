from pydantic import BaseModel, ConfigDict
from schemas.payments import PaymentIDShema
from datetime import date

class TimeShema(BaseModel):
    regular_hours: str 
    regular_min: str  

    over_hours: str   
    over_min: str 

    meal_hours: str     
    meal_min: str   
    holiday_hours: str
    holiday_min: str
    sick_hours: str
    sick_min: str
    commissions :float
    concessions :float
    vacations_hours: str  
    vacations_min: str  
    sick_pay: float
    regular_pay: float
    holyday_pay: float
    vacation_pay:float
    meal_time_pay: float
    overtime_pay:float 
    tips: float
    payments: list[PaymentIDShema]
     

    model_config : ConfigDict(from_attributes=True)


class TimeIDShema(TimeShema):
    created_at : date
    id: int
   

