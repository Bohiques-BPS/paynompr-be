from pydantic import BaseModel, ConfigDict


class PaymentShema(BaseModel):
    name : str
    amount : float  
    model_config : ConfigDict(from_attributes=True)


class PaymentIDShema(PaymentShema):
    id: int
   

