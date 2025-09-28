from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.models import Alert, User
from app.schemas.schemas import AlertCreate, AlertRead


router = APIRouter()


@router.post("/", response_model=AlertRead)
def create_alert(payload: AlertCreate, db: Session = Depends(get_db)):
    user = db.query(User).get(payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    alert = Alert(**payload.dict())
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


@router.get("/", response_model=list[AlertRead])
def list_alerts(user_id: int | None = None, db: Session = Depends(get_db)):
    q = db.query(Alert)
    if user_id is not None:
        q = q.filter(Alert.user_id == user_id)
    return q.order_by(Alert.timestamp.desc()).all()


@router.patch("/{alert_id}", response_model=AlertRead)
def resolve_alert(alert_id: int, resolved: bool, db: Session = Depends(get_db)):
    alert = db.query(Alert).get(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.resolved = resolved
    db.commit()
    db.refresh(alert)
    return alert


@router.delete("/{alert_id}")
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).get(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    db.delete(alert)
    db.commit()
    return {"ok": True}

