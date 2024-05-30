from pydantic import BaseModel
from datetime import date
from schemas.time import TimeIDShema

class OutEmployersSchema(BaseModel):    
    
    last_name: str | None = None  
    mother_last_name: str | None = None  
    first_name: str | None = None  
    middle_name: str | None = None
    email: str | None = None
    account_number : str | None = None

    type_entity:  int | None = None 
    gender:  int | None = None
    birthday:date | None = None
    fax : str | None = None 
    website : str | None = None 
    withholding: str | None = None 
    merchant_register : str | None = None 
    employer_id: str | None = None 
    bank_account: str | None = None  
    address: str | None = None  
    address_state: str | None = None  
    address_country: str | None = None  
    address_number: str | None = None  
    phone_number: str | None = None  
    smartphone_number: str | None = None 


class OutEmployerReturnIDShema(OutEmployersSchema):
    is_deleted: bool | None = None 
    id : int



