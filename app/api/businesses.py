from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", tags=["Enhancements"])
def list_businesses(db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT * FROM businesses")).mappings().all()
    return list(rows)
