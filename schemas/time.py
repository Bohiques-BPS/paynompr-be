from pydantic import BaseModel, ConfigDict
from schemas.payments import PaymentIDShema

class TimeShema(BaseModel):
    regular_time : int
    overtime : int
    meal_time : int
    sick_hours : int
    vacations_hours :  int
    disability : float
    medicare: float
    regular_pay: float
    payments: list[PaymentIDShema]
     

    model_config : ConfigDict(from_attributes=True)


class TimeIDShema(TimeShema):
    id: int
   

