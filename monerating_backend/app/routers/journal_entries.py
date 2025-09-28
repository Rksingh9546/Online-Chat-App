from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.models import JournalEntry, User
from app.schemas.schemas import JournalEntryCreate, JournalEntryRead


router = APIRouter()


@router.post("/", response_model=JournalEntryRead)
def create_journal_entry(payload: JournalEntryCreate, db: Session = Depends(get_db)):
    user = db.query(User).get(payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    entry = JournalEntry(**payload.dict())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.get("/", response_model=list[JournalEntryRead])
def list_journal_entries(user_id: int | None = None, db: Session = Depends(get_db)):
    q = db.query(JournalEntry)
    if user_id is not None:
        q = q.filter(JournalEntry.user_id == user_id)
    return q.order_by(JournalEntry.timestamp.desc()).all()


@router.delete("/{entry_id}")
def delete_journal_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(JournalEntry).get(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    db.delete(entry)
    db.commit()
    return {"ok": True}

