from pydantic import BaseModel, Field, ConfigDict

class TaxeShema(BaseModel):
    name: str
    amount: float = Field(..., ge=0.0)  
    required: float = Field(..., ge=0.0) 
    type_taxe: float
    type_amount: float
    model_config: ConfigDict

class TaxeIDShema(TaxeShema):
    id: int
