from sqlalchemy import Column, String, Text, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


class NewsArticle(Base):
    __tablename__ = "articles"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text)
    url = Column(String, unique=True, nullable=False)
    source = Column(String, nullable=False)
    category = Column(String, nullable=False)
    published_at = Column(DateTime, nullable=False)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    content = Column(Text)
    image_url = Column(String)
    
    def __repr__(self):
        return f"<NewsArticle {self.title[:50]}...>"


class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<ChatSession {self.id}>"


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, nullable=False)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ChatMessage {self.role} in {self.session_id}>"
