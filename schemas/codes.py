from pydantic import BaseModel, ConfigDict


class CodeSchema(BaseModel):
    code: str

    owner: str | None = None
    amount: int

    model_config = ConfigDict(from_attributes=True)
