from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import engine, Base, SessionLocal
from .models import Phone
from .schemas import PhoneCreate, PhoneResponse

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