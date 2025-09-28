from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.models import MoodLog, JournalEntry
from app.services.analytics import compute_sentiment, linear_trend, zscore_anomalies


router = APIRouter()


@router.post("/sentiment")
def sentiment(text: str) -> dict[str, float]:
    return {"compound": compute_sentiment(text)}


@router.get("/mood-trend/{user_id}")
def mood_trend(user_id: int, db: Session = Depends(get_db)) -> dict[str, float]:
    logs = db.query(MoodLog).filter(MoodLog.user_id == user_id).order_by(MoodLog.timestamp.asc()).all()
    scores = [log.mood_score for log in logs]
    return {"slope": linear_trend(scores)}


@router.get("/mood-anomalies/{user_id}")
def mood_anomalies(user_id: int, db: Session = Depends(get_db)) -> dict[str, list[int] | float]:
    logs = db.query(MoodLog).filter(MoodLog.user_id == user_id).order_by(MoodLog.timestamp.asc()).all()
    scores = [log.mood_score for log in logs]
    res = zscore_anomalies(scores)
    return {"indices": res.indices, "z_threshold": res.threshold}

