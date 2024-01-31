


from pydantic import BaseModel, ConfigDict


class Accountants(BaseModel):
    code_id: int | None = None
    email: str | None = None
    name: str | None = None
    middle_name: str | None = None
    first_last_name: str | None = None
    second_last_name: str | None = None
    company: str | None = None
    phone: str | None = None
    country: str | None = None
    state: str | None = None
    zip_code: str | None = None
    identidad_ssa: str | None = None
    identidad_bso: str | None = None
    identidad_efile: str | None = None
    address: str | None = None
    employer_insurance_number : str | None = None
    user_id: int | None = None