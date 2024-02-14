from pydantic import BaseModel, ConfigDict


class TimeShema(BaseModel):
    regular_time : int
    overtime : int
    meal_time : int
    sick_hours : int
    vacations_hours :  int
    disability : float
    medicare: float
    regular_pay: float
     

    model_config : ConfigDict(from_attributes=True)


class TimeIDShema(TimeShema):
    id: int
   

