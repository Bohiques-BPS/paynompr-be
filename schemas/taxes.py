from pydantic import BaseModel, ConfigDict


class TaxeShema(BaseModel):
    name : str
    amount : float  
    model_config : ConfigDict(from_attributes=True)


class TaxeIDShema(TaxeShema):
    id: int
   

