from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.models import WearableReading, User
from app.schemas.schemas import WearableReadingCreate, WearableReadingRead


router = APIRouter()


@router.post("/", response_model=WearableReadingRead)
def create_wearable_reading(payload: WearableReadingCreate, db: Session = Depends(get_db)):
    user = db.query(User).get(payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    reading = WearableReading(**payload.dict())
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return reading


@router.get("/", response_model=list[WearableReadingRead])
def list_wearable_readings(user_id: int | None = None, db: Session = Depends(get_db)):
    q = db.query(WearableReading)
    if user_id is not None:
        q = q.filter(WearableReading.user_id == user_id)
    return q.order_by(WearableReading.timestamp.desc()).all()


@router.delete("/{reading_id}")
def delete_wearable_reading(reading_id: int, db: Session = Depends(get_db)):
    reading = db.query(WearableReading).get(reading_id)
    if not reading:
        raise HTTPException(status_code=404, detail="Reading not found")
    db.delete(reading)
    db.commit()
    return {"ok": True}

