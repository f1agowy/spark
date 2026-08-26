import logging
from datetime import datetime
from typing import Dict, List
from database.db import SessionLocal
from database.models import SavedArticle
from sqlalchemy import func
from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)


class StatsService:
    """
    Service for calculating yearly statistics
    """
    
    async def get_stats(self) -> Dict:
        """Get comprehensive statistics"""
        try:
            db = SessionLocal()
            
            # Total articles
            total = db.query(func.count(SavedArticle.id)).scalar() or 0
            
            # Articles by month
            articles_by_month = {}
            for month in range(1, 13):
                count = db.query(func.count(SavedArticle.id)).filter(
                    func.extract('month', SavedArticle.saved_at) == month,
                    func.extract('year', SavedArticle.saved_at) == datetime.now().year
                ).scalar() or 0
                month_name = [
                    'Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec',
                    'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień'
                ][month - 1]
                articles_by_month[month_name] = count
            
            # Top tags
            top_tags = {}
            articles = db.query(SavedArticle.tags).filter(SavedArticle.tags.isnot(None)).all()
            for article in articles:
                if article[0]:
                    tags = article[0].split(',')
                    for tag in tags:
                        tag = tag.strip()
                        top_tags[tag] = top_tags.get(tag, 0) + 1
            
            sorted_tags = sorted(top_tags.items(), key=lambda x: x[1], reverse=True)[:10]
            
            # Articles by source
            sources = db.query(
                SavedArticle.source,
                func.count(SavedArticle.id).label('count')
            ).group_by(SavedArticle.source).all()
            
            sources_dict = {source: count for source, count in sources}
            
            # Articles by category
            categories = db.query(
                SavedArticle.category,
                func.count(SavedArticle.id).label('count')
            ).group_by(SavedArticle.category).all()
            
            categories_dict = {cat: count for cat, count in categories}
            
            # Recent articles
            recent = db.query(SavedArticle).order_by(
                SavedArticle.saved_at.desc()
            ).limit(5).all()
            
            db.close()
            
            logger.info(f"📊 Stats calculated: {total} articles total")
            
            return {
                "total_articles": total,
                "articles_by_month": articles_by_month,
                "top_tags": dict(sorted_tags),
                "sources": sources_dict,
                "categories": categories_dict,
                "recent_articles": [
                    {
                        "title": a.title,
                        "saved_at": a.saved_at.isoformat(),
                        "category": a.category
                    }
                    for a in recent
                ]
            }
        
        except Exception as e:
            logger.error(f"❌ Stats error: {str(e)}")
            return {}
