from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.db.database import Base


class ReviewRecord(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    language = Column(String(100), nullable=True)
    provider = Column(String(100), nullable=False)
    score = Column(Integer, nullable=True)
    summary = Column(Text, nullable=False)
    findings_json = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
