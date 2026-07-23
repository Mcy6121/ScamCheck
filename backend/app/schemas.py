from pydantic import BaseModel


class PhoneCreate(BaseModel):
    phone_number: str


class PhoneResponse(BaseModel):
    id: int
    phone_number: str

    class Config:
        from_attributes = True

class ReportCreate(BaseModel):
    phone_number: str
    report_text: str


class ReportResponse(BaseModel):
    id: int
    phone_id: int
    report_text: str
    category: str

    class Config:
        from_attributes = True

class ReportListResponse(BaseModel):
    id: int
    report_text: str
    category: str

    class Config:
        from_attributes = True

class PhoneAnalysis(BaseModel):
    phone_number: str
    report_count: int
    risk_score: int

    class Config:
        from_attributes = True