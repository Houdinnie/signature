from sqlalchemy import Column, Integer, String, DateTime, Text, Date
from sqlalchemy.sql import func
from .base import Base


class DailyReport(Base):
    __tablename__ = "daily_reports"

    id = Column(Integer, primary_key=True, index=True)
    report_date = Column(Date, unique=True, nullable=False)
    morning_plan = Column(Text)
    evening_summary = Column(Text)
    tasks_planned = Column(Integer, server_default="0")
    tasks_completed = Column(Integer, server_default="0")
    tasks_failed = Column(Integer, server_default="0")
    metrics_snapshot = Column(Text)
    insights = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
