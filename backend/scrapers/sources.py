from scrapers.base_scraper import BaseScraper
from typing import List, Dict
from datetime import datetime
import logging
import re

logger = logging.getLogger(__name__)


class EuractivScraper(BaseScraper):
    def __init__(self):
        super().__init__("Euractiv", "https://www.euractiv.com/")
    
    async def scrape(self) -> List[Dict]:
        logger.info("🔄 Scraping Euractiv...")
        try:
            soup = self.fetch_page("https://www.euractiv.com/section/transport-environment/")
            if not soup:
                return []
            
            articles = []
            for item in soup.find_all("article", limit=15):
                try:
                    title_elem = item.find("h2") or item.find("h3")
                    link_elem = item.find("a", href=True)
                    desc_elem = item.find("p")
                    
                    if title_elem and link_elem:
                        articles.append({
                            "title": title_elem.get_text(strip=True),
                            "url": link_elem["href"],
                            "description": desc_elem.get_text(strip=True)[:200] if desc_elem else "",
                            "published_at": datetime.now(),
                            "source": "Euractiv"
                        })
                except Exception as e:
                    logger.debug(f"Error parsing: {e}")
            
            logger.info(f"✅ Found {len(articles)} on Euractiv")
            return articles
        except Exception as e:
            logger.error(f"❌ Euractiv error: {str(e)}")
            return []


class ElectriveScraper(BaseScraper):
    def __init__(self):
        super().__init__("Electrive", "https://www.electrive.com/")
    
    async def scrape(self) -> List[Dict]:
        logger.info("🔄 Scraping Electrive...")
        try:
            soup = self.fetch_page("https://www.electrive.com/")
            if not soup:
                return []
            
            articles = []
            for item in soup.find_all("article", limit=15):
                try:
                    title_elem = item.find("h2") or item.find("h3")
                    link_elem = item.find("a", href=True)
                    desc_elem = item.find("p")
                    
                    if title_elem and link_elem:
                        url = link_elem["href"]
                        if not url.startswith("http"):
                            url = "https://www.electrive.com" + url
                        
                        articles.append({
                            "title": title_elem.get_text(strip=True),
                            "url": url,
                            "description": desc_elem.get_text(strip=True)[:200] if desc_elem else "",
                            "published_at": datetime.now(),
                            "source": "Electrive"
                        })
                except Exception as e:
                    logger.debug(f"Error parsing: {e}")
            
            logger.info(f"✅ Found {len(articles)} on Electrive")
            return articles
        except Exception as e:
            logger.error(f"❌ Electrive error: {str(e)}")
            return []


class AceaScraper(BaseScraper):
    def __init__(self):
        super().__init__("ACEA", "https://www.acea.auto/")
    
    async def scrape(self) -> List[Dict]:
        logger.info("🔄 Scraping ACEA...")
        try:
            soup = self.fetch_page("https://www.acea.auto/")
            if not soup:
                return []
            
            articles = []
            for item in soup.find_all(["article", "div"], class_=re.compile("post|news", re.I), limit=15):
                try:
                    title_elem = item.find(["h2", "h3", "h4"])
                    link_elem = item.find("a", href=True)
                    desc_elem = item.find("p")
                    
                    if title_elem and link_elem:
                        url = link_elem["href"]
                        if not url.startswith("http"):
                            url = "https://www.acea.auto" + url
                        
                        articles.append({
                            "title": title_elem.get_text(strip=True),
                            "url": url,
                            "description": desc_elem.get_text(strip=True)[:200] if desc_elem else "",
                            "published_at": datetime.now(),
                            "source": "ACEA"
                        })
                except Exception as e:
                    logger.debug(f"Error parsing: {e}")
            
            logger.info(f"✅ Found {len(articles)} on ACEA")
            return articles
        except Exception as e:
            logger.error(f"❌ ACEA error: {str(e)}")
            return []


class TransportEnvironmentScraper(BaseScraper):
    def __init__(self):
        super().__init__("Transport & Environment", "https://www.transportenvironment.org/")
    
    async def scrape(self) -> List[Dict]:
        logger.info("🔄 Scraping Transport & Environment...")
        try:
            soup = self.fetch_page("https://www.transportenvironment.org/")
            if not soup:
                return []
            
            articles = []
            for item in soup.find_all("article", limit=15):
                try:
                    title_elem = item.find(["h2", "h3"])
                    link_elem = item.find("a", href=True)
                    desc_elem = item.find("p")
                    
                    if title_elem and link_elem:
                        url = link_elem["href"]
                        if not url.startswith("http"):
                            url = "https://www.transportenvironment.org" + url
                        
                        articles.append({
                            "title": title_elem.get_text(strip=True),
                            "url": url,
                            "description": desc_elem.get_text(strip=True)[:200] if desc_elem else "",
                            "published_at": datetime.now(),
                            "source": "Transport & Environment"
                        })
                except Exception as e:
                    logger.debug(f"Error parsing: {e}")
            
            logger.info(f"✅ Found {len(articles)} on T&E")
            return articles
        except Exception as e:
            logger.error(f"❌ T&E error: {str(e)}")
            return []


class ICCTScraper(BaseScraper):
    def __init__(self):
        super().__init__("ICCT", "https://theicct.org/")
    
    async def scrape(self) -> List[Dict]:
        logger.info("🔄 Scraping ICCT...")
        try:
            soup = self.fetch_page("https://theicct.org/")
            if not soup:
                return []
            
            articles = []
            for item in soup.find_all(["article", "div"], class_=re.compile("post|news", re.I), limit=15):
                try:
                    title_elem = item.find(["h2", "h3"])
                    link_elem = item.find("a", href=True)
                    desc_elem = item.find("p")
                    
                    if title_elem and link_elem:
                        url = link_elem["href"]
                        if not url.startswith("http"):
                            url = "https://theicct.org" + url
                        
                        articles.append({
                            "title": title_elem.get_text(strip=True),
                            "url": url,
                            "description": desc_elem.get_text(strip=True)[:200] if desc_elem else "",
                            "published_at": datetime.now(),
                            "source": "ICCT"
                        })
                except Exception as e:
                    logger.debug(f"Error parsing: {e}")
            
            logger.info(f"✅ Found {len(articles)} on ICCT")
            return articles
        except Exception as e:
            logger.error(f"❌ ICCT error: {str(e)}")
            return []


class AltFuelObservatoryScraper(BaseScraper):
    def __init__(self):
        super().__init__("Alt Fuel Observatory", "https://alternative-fuels-observatory.ec.europa.eu/")
    
    async def scrape(self) -> List[Dict]:
        logger.info("🔄 Scraping Alt Fuel Observatory...")
        try:
            soup = self.fetch_page("https://alternative-fuels-observatory.ec.europa.eu/")
            if not soup:
                return []
            
            articles = []
            for item in soup.find_all(["article", "div"], class_=re.compile("news|post", re.I), limit=15):
                try:
                    title_elem = item.find(["h2", "h3"])
                    link_elem = item.find("a", href=True)
                    desc_elem = item.find("p")
                    
                    if title_elem and link_elem:
                        url = link_elem["href"]
                        if not url.startswith("http"):
                            url = "https://alternative-fuels-observatory.ec.europa.eu" + url
                        
                        articles.append({
                            "title": title_elem.get_text(strip=True),
                            "url": url,
                            "description": desc_elem.get_text(strip=True)[:200] if desc_elem else "",
                            "published_at": datetime.now(),
                            "source": "Alt Fuel Observatory"
                        })
                except Exception as e:
                    logger.debug(f"Error parsing: {e}")
            
            logger.info(f"✅ Found {len(articles)} on AFO")
            return articles
        except Exception as e:
            logger.error(f"❌ AFO error: {str(e)}")
            return []
