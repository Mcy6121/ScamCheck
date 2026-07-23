from pydantic import BaseModel


class PhoneCreate(BaseModel):
    phone_number: str


class PhoneResponse(BaseModel):
    id: int
    phone_number: str

    class Config:
        from_attributes = True