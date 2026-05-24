from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from .base import Base


class CompanyConfig(Base):
    __tablename__ = "company_config"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    mission = Column(Text)
    vision = Column(Text)
    description = Column(Text)
    target_market = Column(Text)
    value_prop = Column(Text)
    pricing_model = Column(Text)
    goals = Column(Text)
    kpis = Column(Text)
    website_url = Column(String(512))
    github_repo = Column(String(512))
    product_type = Column(String(100))
    industry = Column(String(100))
    timezone = Column(String(50), server_default="UTC")
    daily_cycle_hour = Column(Integer, server_default="6")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
