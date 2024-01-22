from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    name: str
    lastname: str
    user_code: str
    role_id: int
    email: str
    password: str
    phone: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UserUpdateSchema(BaseModel):
    phone: str | None = None
    role_id: int | None = None
    password: str | None = None

    model_config = ConfigDict(from_attributes=True)
