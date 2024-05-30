from pydantic import BaseModel
from datetime import date
from schemas.time import TimeIDShema

class EmployersSchema(BaseModel):    
    last_name:  str | None = None
    mother_last_name: str | None = None
    first_name:  str | None = None
    middle_name:  str | None = None
    company_id: int | None = None    
    employee_type:  str | None = None
    social_security_number:  str | None = None
    marital_status:  int | None = None
    address:  str | None = None
    address_state:  str | None = None
    address_country:  str | None = None
    address_number:  str | None = None
    phone_number:  str | None = None
    smartphone_number:  str | None = None
    marbete:  str | None = None
    type:  int | None = None
    date_marb:  date | None = None
    clipboard:  str | None = None
    exec_personal:  int | None = None
    choferil:  str | None = None
    regular_time:  float | None = None
    period_norma:  int | None = None
    licence:  str | None = None
    category_cfse:  str | None = None
    gender:  int | None = None
    birthday:  date | None = None
    date_admission:  date | None = None
    date_egress:  date | None = None
    overtime:  float | None = None
    mealtime:  float | None = None
    vacation_hours:  int | None = None
    vacation_date:  date | None = None
    sicks_hours:  int | None = None
    sicks_date:  date | None = None
    number_dependents:  int | None = None
    shared_custody:  bool | None = None
    number_concessions:  int | None = None
    veteran:  bool | None = None
    type_payroll:  int | None = None
    schedule_type:  int | None = None
    payment_percentage:  str | None = None


class EmployerReturnIDShema(EmployersSchema):
    is_deleted: bool | None = None 
    id : int


class EmployerTimeShema(EmployerReturnIDShema):
    times: list[TimeIDShema] = []    
    class Config:
        orm_mode = True
