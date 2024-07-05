from pydantic import BaseModel, ConfigDict
from schemas.payments import PaymentIDShema
from datetime import date

class TimeShema(BaseModel):
    regular_time: str
    regular_amount: float
    over_amount: float
    meal_amount: float
    over_time: str
    
    meal_time: str 
    holiday_time:str
    sick_time:str
    commissions :float
    concessions :float
    inability:float
    medicare :float
    secure_social :float
    social_tips :float
    tax_pr :float
    choferil:float
    vacations_hours: str  
    vacations_min: str  
    tips: float
    payment: list[PaymentIDShema]
     

    model_config : ConfigDict(from_attributes=True)


class TimeIDShema(TimeShema):
    created_at : date
    id: int

class TimeIDShema2(TimeShema):
    
    id: int
   

   

