from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base


class SocialPost(Base):
    __tablename__ = "social_posts"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50), server_default="twitter")
    content = Column(Text, nullable=False)
    status = Column(String(50), server_default="draft")
    tweet_id = Column(String(100))
    scheduled_for = Column(DateTime(timezone=True))
    published_at = Column(DateTime(timezone=True))
    engagement = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SocialEngagement(Base):
    __tablename__ = "social_engagements"

    id = Column(Integer, primary_key=True, index=True)
    mention_id = Column(String(100), unique=True)
    author_handle = Column(String(100))
    content = Column(Text)
    our_reply = Column(Text)
    reply_id = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
