import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from datetime import datetime
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Base class for all scrapers"""
    
    def __init__(self, source_name: str, url: str):
        self.source_name = source_name
        self.base_url = url
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse HTML page"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, "lxml")
        except Exception as e:
            logger.error(f"❌ Error fetching {url}: {str(e)}")
            return None
    
    @abstractmethod
    async def scrape(self) -> List[Dict]:
        """
        Scrape articles from source
        """
        pass
