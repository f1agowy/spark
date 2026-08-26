import asyncio
import logging
from typing import Dict, List
from datetime import datetime
import os
import requests

from scrapers import (
    EuractivScraper,
    ElectriveScraper,
    AceaScraper,
    TransportEnvironmentScraper,
    ICCTScraper,
    AltFuelObservatoryScraper
)
from services.categorizer import categorize_articles

logger = logging.getLogger(__name__)


class NewsService:
    def __init__(self):
        self.scrapers = [
            EuractivScraper(),
            ElectriveScraper(),
            AceaScraper(),
            TransportEnvironmentScraper(),
            ICCTScraper(),
            AltFuelObservatoryScraper()
        ]
        self.newsapi_key = os.getenv("NEWSAPI_KEY")
    
    async def scrape_european_sources(self) -> List[Dict]:
        logger.info("🌍 Scraping 6 European sources...")
        
        tasks = [scraper.scrape() for scraper in self.scrapers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_articles = []
        for i, result in enumerate(results):
            if isinstance(result, list):
                all_articles.extend(result)
            elif isinstance(result, Exception):
                logger.error(f"Scraper error: {result}")
        
        logger.info(f"✅ Scraped {len(all_articles)} from European sources")
        return all_articles
    
    async def fetch_global_news(self) -> List[Dict]:
        if not self.newsapi_key:
            logger.warning("⚠️ NewsAPI key not configured")
            return []
        
        logger.info("🌐 Fetching global news...")
        
        try:
            queries = [
                "commercial vehicles truck MHCV",
                "electric vehicles EV battery",
                "automotive news"
            ]
            
            all_articles = []
            
            for query in queries:
                url = "https://newsapi.org/v2/everything"
                params = {
                    "q": query,
                    "apiKey": self.newsapi_key,
                    "sortBy": "publishedAt",
                    "language": "en",
                    "pageSize": 5
                }
                
                try:
                    response = requests.get(url, params=params, timeout=10)
                    response.raise_for_status()
                    data = response.json()
                    
                    for article in data.get("articles", []):
                        all_articles.append({
                            "title": article.get("title", ""),
                            "url": article.get("url", ""),
                            "description": article.get("description", ""),
                            "source": article.get("source", {}).get("name", "NewsAPI"),
                            "published_at": datetime.fromisoformat(
                                article.get("publishedAt", "").replace("Z", "+00:00")
                            ),
                        })
                except Exception as e:
                    logger.error(f"Error: {query}: {e}")
            
            logger.info(f"✅ Fetched {len(all_articles)} global articles")
            return all_articles
        
        except Exception as e:
            logger.error(f"❌ NewsAPI error: {str(e)}")
            return []
    
    async def aggregate_news(self, force_refresh: bool = False) -> Dict:
        logger.info("📰 Starting aggregation...")
        
        try:
            european = await self.scrape_european_sources()
            global_news = await self.fetch_global_news()
            
            all_articles = european + global_news
            
            seen_urls = set()
            unique_articles = []
            for article in all_articles:
                url = article.get("url", "")
                if url not in seen_urls and url:
                    seen_urls.add(url)
                    unique_articles.append(article)
            
            categorized = categorize_articles(unique_articles)
            
            return {
                "europe_mhcv": categorized["europe_mhcv"],
                "europe_other": categorized["europe_other"],
                "global": categorized["global"],
                "all_news": unique_articles,
                "aggregated_at": datetime.now().isoformat(),
                "total_articles": len(unique_articles)
            }
        
        except Exception as e:
            logger.error(f"❌ Aggregation error: {str(e)}")
            raise
