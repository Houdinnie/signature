from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base


class AdCampaign(Base):
    __tablename__ = "ad_campaigns"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50), nullable=False)
    external_id = Column(String(255))
    name = Column(String(512), nullable=False)
    goal = Column(String(255))
    status = Column(String(50), server_default="active")
    daily_budget_cents = Column(Integer, server_default="0")
    total_spent_cents = Column(Integer, server_default="0")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    metrics = relationship("AdMetric", back_populates="campaign")


class AdMetric(Base):
    __tablename__ = "ad_metrics"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("ad_campaigns.id"), nullable=False)
    date = Column(Date, nullable=False)
    impressions = Column(Integer, server_default="0")
    clicks = Column(Integer, server_default="0")
    conversions = Column(Integer, server_default="0")
    spend_cents = Column(Integer, server_default="0")
    ctr = Column(Float, server_default="0")
    cpc_cents = Column(Integer, server_default="0")
    roas = Column(Float, server_default="0")

    campaign = relationship("AdCampaign", back_populates="metrics")
