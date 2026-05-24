from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    message_type = Column(String(50), nullable=False)
    priority = Column(String(20), server_default="medium")
    status = Column(String(20), server_default="pending")
    subject = Column(String(512))
    body = Column(Text)
    metadata_json = Column(Text)
    thread_id = Column(String(255))
    reply_to_id = Column(Integer, ForeignKey("messages.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    delivered_at = Column(DateTime(timezone=True))
    read_at = Column(DateTime(timezone=True))

    sender = relationship("Agent", foreign_keys=[sender_id])
    receiver = relationship("Agent", foreign_keys=[receiver_id])
    replies = relationship("Message", backref="parent", remote_side=[id])
