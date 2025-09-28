from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Float, Boolean
from sqlalchemy.orm import relationship

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    timezone = Column(String(64), default="UTC")
    created_at = Column(DateTime, default=datetime.utcnow)

    mood_logs = relationship("MoodLog", back_populates="user", cascade="all, delete-orphan")
    journal_entries = relationship("JournalEntry", back_populates="user", cascade="all, delete-orphan")
    wearable_readings = relationship("WearableReading", back_populates="user", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="user", cascade="all, delete-orphan")


class MoodLog(Base):
    __tablename__ = "mood_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    mood_score = Column(Integer, nullable=False)  # 1-10
    mood_tags = Column(String(255), default="")  # comma-separated tags
    note_text = Column(Text, default="")
    sentiment_score = Column(Float, nullable=True)

    user = relationship("User", back_populates="mood_logs")


class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    text = Column(Text, default="")
    sentiment_score = Column(Float, nullable=True)
    keywords = Column(String(255), default="")

    user = relationship("User", back_populates="journal_entries")


class WearableReading(Base):
    __tablename__ = "wearable_readings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    type = Column(String(64), nullable=False)  # heart_rate, steps, sleep, etc
    value = Column(Float, nullable=False)
    device = Column(String(64), default="unknown")

    user = relationship("User", back_populates="wearable_readings")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    type = Column(String(64), nullable=False)
    message = Column(Text, nullable=False)
    resolved = Column(Boolean, default=False)

    user = relationship("User", back_populates="alerts")

