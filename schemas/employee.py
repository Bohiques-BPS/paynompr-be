from pydantic import BaseModel


class EmployersSchema(BaseModel):
   
    last_name:  str | None = None
    mother_last_name: str | None = None
    first_name:  str | None = None
    middle_name:  str | None = None
    company_id: int | None = None    
    employee_type:  str | None = None
    social_security_number:  str | None = None
    marital_status:  str | None = None
    address:  str | None = None
    address_state:  str | None = None
    address_country:  str | None = None
    address_number:  str | None = None
    phone_number:  str | None = None
    smartphone_number:  str | None = None