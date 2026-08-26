from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import os
from dotenv import load_dotenv
import logging
import asyncio

from database.db import init_db
from services.news_service import NewsService
from services.ai_service import AIService

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="SPARK - MHCV News Agent", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Services
news_service = NewsService()
ai_service = AIService()


class ChatMessage(BaseModel):
    message: str
    session_id: str


class NewsRequest(BaseModel):
    force_refresh: bool = False


@app.on_event("startup")
async def startup():
    """Initialize database on startup"""
    init_db()
    logger.info("✅ Database initialized")


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


@app.post("/api/news/fetch")
async def fetch_news(request: NewsRequest):
    """
    Fetch and analyze news from all sources
    Returns categorized news: Europe-MHCV, Europe-Other, Global
    """
    try:
        logger.info("🔄 Starting news aggregation...")
        
        # Fetch news
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


@app.post("/api/chat")
async def chat(request: ChatMessage):
    """
    Chat endpoint - ask questions about fetched news
    """
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        logger.info(f"💬 New chat message from session {request.session_id[:8]}...")
        
        # Get response from AI
        response = await ai_service.chat(request.message, request.session_id)
        
        return {
            "success": True,
            "response": response,
            "session_id": request.session_id,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sessions/{session_id}")
async def get_session_history(session_id: str):
    """
    Get chat history for a session
    """
    try:
        history = ai_service.get_session_history(session_id)
        return {"session_id": session_id, "messages": history}
    except Exception as e:
        logger.error(f"❌ Error retrieving session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
