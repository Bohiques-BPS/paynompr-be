from pydantic import BaseModel, ConfigDict
from datetime import date
from schemas.employee import EmployerReturnIDShema

class CompaniesSchema(BaseModel):    
    
    name: str | None = None    
    commercial_register: str | None = None    
    jurisdiction: str | None = None    
    accountant_id: int | None = None
    email: str | None = None
    contact: str | None = None
    contact_number: str | None = None
    website: str | None = None
    postal_address: str | None = None
    zipcode_postal_address: str | None = None
    country_postal_address: str | None = None
    state_postal_addess: str | None = None    
    physical_address: str | None = None
    zipcode_physical_address: str | None = None
    country_physical_address: str | None = None
    state_physical_address: str | None = None
    phone_number: str | None = None
    fax_number: str | None = None
    industrial_code: str | None = None
    payer: str | None = None
    desem: str | None = None
    number_patronal: str | None = None
    coml : date | None = None

    disabled_percent: str | None = None
    driver: str | None = None
    polize_number: str | None = None
    driver_code: str | None = None
    driver_rate: str | None = None

    model_config = ConfigDict(from_attributes=True)


class CompaniesIdSchema(CompaniesSchema):
    id: int

class CompaniesWithEmployersSchema(CompaniesIdSchema): 
    employers: list[EmployerReturnIDShema] = []    
    class Config:
        orm_mode = True
      


