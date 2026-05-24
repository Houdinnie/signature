from sqlalchemy import Column, Integer, String, DateTime, Text, Date, ForeignKey
from sqlalchemy.sql import func
from .base import Base


class StripeEvent(Base):
    __tablename__ = "stripe_events"

    id = Column(Integer, primary_key=True, index=True)
    stripe_event_id = Column(String(255), unique=True, nullable=False)
    event_type = Column(String(255), nullable=False, index=True)
    customer_id = Column(String(255))
    amount_cents = Column(Integer)
    currency = Column(String(10))
    status = Column(String(50), server_default="processed")
    raw_payload = Column(Text)
    processed_at = Column(DateTime(timezone=True), server_default=func.now())


class RevenueSnapshot(Base):
    __tablename__ = "revenue_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    snapshot_date = Column(Date, unique=True, nullable=False, index=True)
    mrr_cents = Column(Integer, server_default="0")
    arr_cents = Column(Integer, server_default="0")
    active_subscribers = Column(Integer, server_default="0")
    churned_today = Column(Integer, server_default="0")
    new_today = Column(Integer, server_default="0")
    total_revenue_month_cents = Column(Integer, server_default="0")
    stripe_balance_cents = Column(Integer, server_default="0")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ExpenseRecord(Base):
    __tablename__ = "expense_records"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100), nullable=False)
    vendor = Column(String(255), nullable=False)
    amount_cents = Column(Integer, nullable=False)
    currency = Column(String(10), server_default="usd")
    description = Column(Text)
    date = Column(Date, nullable=False)
    external_ref = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
