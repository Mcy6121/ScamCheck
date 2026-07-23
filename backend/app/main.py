from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .ai import calculate_risk

from .database import engine, Base, SessionLocal
from .models import Phone
from .schemas import PhoneCreate, PhoneResponse

from .models import Phone, Report
from .schemas import (
    PhoneCreate,
    PhoneResponse,
    ReportCreate,
    ReportResponse,
    ReportListResponse,
    PhoneAnalysis,
)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ScamCheck API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"status": "online"}


@app.post("/phones", response_model=PhoneResponse)
def create_phone(phone: PhoneCreate, db: Session = Depends(get_db)):
    db_phone = Phone(phone_number=phone.phone_number)

    db.add(db_phone)
    db.commit()
    db.refresh(db_phone)

    return db_phone

from fastapi import HTTPException

@app.get("/phones/{phone_number}", response_model=PhoneResponse)
def get_phone(phone_number: str, db: Session = Depends(get_db)):

    phone = db.query(Phone).filter(
        Phone.phone_number == phone_number
    ).first()

    if phone is None:
        raise HTTPException(
            status_code=404,
            detail="Telefon numarası bulunamadı."
        )

    return phone


@app.post("/reports", response_model=ReportResponse)
def create_report(report: ReportCreate, db: Session = Depends(get_db)):

    phone = db.query(Phone).filter(
        Phone.phone_number == report.phone_number
    ).first()

    if phone is None:
        raise HTTPException(
            status_code=404,
            detail="Telefon numarası bulunamadı."
        )

    db_report = Report(
        phone_id=phone.id,
        report_text=report.report_text
    )

    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    return db_report

from typing import List

@app.get(
    "/reports/{phone_number}",
    response_model=List[ReportListResponse]
)
def get_reports(phone_number: str, db: Session = Depends(get_db)):

    phone = db.query(Phone).filter(
        Phone.phone_number == phone_number
    ).first()

    if phone is None:
        raise HTTPException(
            status_code=404,
            detail="Telefon bulunamadı."
        )

    reports = db.query(Report).filter(
        Report.phone_id == phone.id
    ).all()

    return reports


@app.get("/analysis/{phone_number}", response_model=PhoneAnalysis)
def analyze_phone(phone_number: str, db: Session = Depends(get_db)):

    phone = db.query(Phone).filter(
        Phone.phone_number == phone_number
    ).first()

    if phone is None:
        raise HTTPException(
            status_code=404,
            detail="Telefon bulunamadı."
        )

    reports = db.query(Report).filter(
        Report.phone_id == phone.id
    ).all()

    risk = calculate_risk(len(reports))

    return {
        "phone_number": phone.phone_number,
        "report_count": len(reports),
        "risk_score": risk
    }