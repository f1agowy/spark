from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import os
from dotenv import load_dotenv
import logging
import asyncio
from typing import List, Optional

from database.db import init_db, SessionLocal
from database.models import SavedArticle, ChatMessage
from services.news_service import NewsService
from services.ai_service import AIService
from services.library_service import LibraryService
from services.stats_service import StatsService

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MOBGLO - MHCV News Agent", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://mobglo.onrender.com",
        os.getenv("FRONTEND_URL", "http://localhost:3000")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Services
news_service = NewsService()
ai_service = AIService()
library_service = LibraryService()
stats_service = StatsService()


class ChatMessage(BaseModel):
    message: str
    session_id: str
    article_context: Optional[str] = None  # Opcjonalnie - kontekst artykułu


class NewsRequest(BaseModel):
    force_refresh: bool = False


class SaveArticleRequest(BaseModel):
    title: str
    url: str
    source: str
    description: str
    category: str
    user_note: str = ""
    tags: str = ""  # #EURO7,#REGULACJE


class UpdateArticleRequest(BaseModel):
    user_note: Optional[str] = None
    tags: Optional[str] = None
    ai_generated_note: Optional[str] = None


class AIEnhanceNoteRequest(BaseModel):
    article_id: str
    current_note: str
    article_title: str
    prompt: str = "Rozwiń tę notatkę z bardziej szczegółową analizą"


@app.on_event("startup")
async def startup():
    """Initialize database on startup"""
    init_db()
    logger.info("✅ Database initialized")


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


@app.post("/news/fetch")
async def fetch_news(request: NewsRequest):
    """
    Fetch and analyze news from all sources
    """
    try:
        logger.info("🔄 Starting news aggregation...")
        
        news_data = await news_service.aggregate_news(force_refresh=request.force_refresh)
        
        logger.info(f"✅ Fetched {len(news_data.get('all_news', []))} articles")
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "data": news_data,
            "categories": {
                "europe_mhcv": len(news_data.get("europe_mhcv", [])),
                "europe_other": len(news_data.get("europe_other", [])),
                "global": len(news_data.get("global", [])),
            }
        }
    except Exception as e:
        logger.error(f"❌ Error fetching news: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat")
async def chat(request: ChatMessage):
    """
    Chat endpoint - ask questions about fetched news or general topics
    """
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        logger.info(f"💬 Chat message from session {request.session_id[:8]}...")
        
        response = await ai_service.chat(
            request.message,
            request.session_id,
            article_context=request.article_context
        )
        
        return {
            "success": True,
            "response": response,
            "session_id": request.session_id,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/library/save")
async def save_article(request: SaveArticleRequest):
    """
    Save article to library (roczna biblioteka)
    """
    try:
        logger.info(f"💾 Saving article: {request.title[:50]}...")
        
        article = await library_service.save_article(
            title=request.title,
            url=request.url,
            source=request.source,
            description=request.description,
            category=request.category,
            user_note=request.user_note,
            tags=request.tags
        )
        
        logger.info(f"✅ Article saved: {article.id}")
        
        return {
            "success": True,
            "article_id": article.id,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Save error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/library/all")
async def get_all_articles(month: Optional[int] = None, tag: Optional[str] = None):
    """
    Get all saved articles (biblioteka roczna) with optional filters
    """
    try:
        logger.info(f"📚 Getting library articles (month={month}, tag={tag})")
        
        articles = await library_service.get_articles(month=month, tag=tag)
        
        return {
            "success": True,
            "articles": articles,
            "total": len(articles),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Error getting articles: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/library/{article_id}")
async def update_article(article_id: str, request: UpdateArticleRequest):
    """
    Update article note or tags
    """
    try:
        logger.info(f"✏️ Updating article: {article_id}")
        
        article = await library_service.update_article(
            article_id=article_id,
            user_note=request.user_note,
            tags=request.tags,
            ai_generated_note=request.ai_generated_note
        )
        
        logger.info(f"✅ Article updated")
        
        return {
            "success": True,
            "article_id": article.id,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Update error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/library/{article_id}")
async def delete_article(article_id: str):
    """
    Delete article from library
    """
    try:
        logger.info(f"🗑️ Deleting article: {article_id}")
        
        await library_service.delete_article(article_id)
        
        logger.info(f"✅ Article deleted")
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Delete error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/library/{article_id}/enhance-note")
async def enhance_note(article_id: str, request: AIEnhanceNoteRequest):
    """
    Ask AI to enhance/expand the note for an article
    """
    try:
        logger.info(f"✨ Enhancing note for article: {article_id}")
        
        enhanced_note = await ai_service.enhance_note(
            current_note=request.current_note,
            article_title=request.article_title,
            prompt=request.prompt
        )
        
        logger.info(f"✅ Note enhanced")
        
        return {
            "success": True,
            "enhanced_note": enhanced_note,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Enhancement error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def get_statistics():
    """
    Get yearly statistics
    """
    try:
        logger.info("📊 Getting statistics")
        
        stats = await stats_service.get_stats()
        
        return {
            "success": True,
            "stats": stats,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Stats error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/library/export/excel")
async def export_excel():
    """
    Export all articles to Excel
    """
    try:
        logger.info("📥 Exporting to Excel")
        
        file_path = await library_service.export_excel()
        
        logger.info(f"✅ Excel exported")
        
        return {
            "success": True,
            "message": "Export ready",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Export error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
