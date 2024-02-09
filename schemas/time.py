from pydantic import BaseModel, ConfigDict


class TimeShema(BaseModel):
    regular_time : str
    overtime : str
    meal_time : str
    sick_hours : str
    sick_vacations :  str

    model_config : ConfigDict(from_attributes=True)


class TimeIDShema(TimeShema):
    id: int
   

