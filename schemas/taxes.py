from pydantic import BaseModel, ConfigDict


class TaxeShema(BaseModel):
    name : str
    amount : float  
    requiered: float  
    type_taxe: float
    type_amount: float
    model_config : ConfigDict(from_attributes=True)


class TaxeIDShema(TaxeShema):
    id: int
   

