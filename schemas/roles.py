from pydantic import BaseModel, ConfigDict


class RoleSchema(BaseModel):
    role: str

    model_config = ConfigDict(from_attributes=True)
