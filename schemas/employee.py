from pydantic import BaseModel
from datetime import date


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
    regular_time:  str | None = None
    period_norma:  int | None = None
    licence:  str | None = None
    category_cfse:  str | None = None
    gender:  int | None = None
    birthday:  date | None = None
    date_admission:  date | None = None
    date_egress:  date | None = None
    about_time:  str | None = None
    mealtime:  str | None = None
    vacation_hours:  str | None = None
    vacation_date:  date | None = None
    number_dependents:  str | None = None
    shared_custody:  str | None = None
    number_concessions:  str | None = None
    veteran:  str | None = None
    type_payroll:  int | None = None
    schedule_type:  int | None = None
    payment_percentage:  str | None = None


class EmployerReturnIDShema(EmployersSchema):
    id : int