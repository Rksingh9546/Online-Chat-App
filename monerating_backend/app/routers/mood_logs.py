from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from app.db.session import get_db
from app.models.models import MoodLog, User
from app.schemas.schemas import MoodLogCreate, MoodLogRead


router = APIRouter()


@router.post("/", response_model=MoodLogRead)
def create_mood_log(payload: MoodLogCreate, db: Session = Depends(get_db)):
    user = db.query(User).get(payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    log = MoodLog(**payload.dict())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@router.get("/", response_model=list[MoodLogRead])
def list_mood_logs(
    user_id: int | None = None,
    limit: int = Query(100, ge=1, le=1000),
    order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    q = db.query(MoodLog)
    if user_id is not None:
        q = q.filter(MoodLog.user_id == user_id)
    q = q.order_by(desc(MoodLog.timestamp) if order == "desc" else asc(MoodLog.timestamp))
    return q.limit(limit).all()


@router.get("/{log_id}", response_model=MoodLogRead)
def get_mood_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(MoodLog).get(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Mood log not found")
    return log


@router.delete("/{log_id}")
def delete_mood_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(MoodLog).get(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Mood log not found")
    db.delete(log)
    db.commit()
    return {"ok": True}

