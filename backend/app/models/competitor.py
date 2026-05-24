from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from .base import Base


class Competitor(Base):
    __tablename__ = "competitors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    website = Column(String(512))
    pricing_info = Column(Text)
    positioning = Column(Text)
    strengths = Column(Text)
    weaknesses = Column(Text)
    last_researched = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
