from pydantic import BaseModel, ConfigDict


class PaymentShema(BaseModel):
    name : str
    amount : float  
    requiered: float  
    type_taxe: float
    is_active: bool | None = None
    type_amount: float
    model_config : ConfigDict(from_attributes=True)


class PaymentIDShema(PaymentShema):
    id: int
   

