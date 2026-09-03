from sqlalchemy import Column, String, Text, DateTime, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


class NewsCache(Base):
    """Cache articles with deduplication - expires after 7 days"""
    __tablename__ = "news_cache"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tier = Column(String, nullable=False)  # "tier1", "tier2", "tier3"
    title = Column(String, nullable=False)
    url = Column(String, nullable=False, unique=True)
    source = Column(String, nullable=False)
    description = Column(Text)
    ai_summary = Column(Text)  # 3-4 sentence summary
    is_oem = Column(Boolean, default=False)  # OEM komunikaty
    is_duplicate = Column(Boolean, default=False)  # Powtórka z poprzednich dni
    published_at = Column(DateTime, nullable=False)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)  # now + 7 days
    
    def __repr__(self):
        return f"<NewsCache {self.tier} {self.title[:50]}...>"


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


class SavedArticle(Base):
    __tablename__ = "saved_articles"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    source = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String, nullable=False)
    user_note = Column(Text)  # Notatka użytkownika
    tags = Column(String)  # Tagi oddzielone przecinkami: #EURO7,#REGULACJE
    saved_at = Column(DateTime, default=datetime.utcnow)
    ai_generated_note = Column(Text)  # Notatka wygenerowana przez AI
    
    def __repr__(self):
        return f"<SavedArticle {self.title[:50]}...>"


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
