import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

EUROP_MHCV_KEYWORDS = [
    "truck", "hvac", "bus", "commercial", "heavy", "medium", "emission",
    "euro", "regulation", "europe", "eu", "alternative fuel", "electric truck",
    "hydrogen", "diesel", "euro 6", "euro 7", "hgv", "vehicle", "co2",
    "mhcv", "n3", "n2", "transport", "decarbonis", "emission standard"
]

GLOBAL_LV_KEYWORDS = [
    "passenger car", "sedan", "suv", "ev", "electric vehicle", "bev",
    "tesla", "battery", "charging", "autonomous", "self-driving", "china", "usa"
]


def categorize_article(title: str, description: str, source: str) -> str:
    """
    Categorize: europe_mhcv, europe_other, or global
    """
    full_text = (title + " " + description).lower()
    
    europe_sources = [
        "euractiv", "acea", "transport", "electrive", "icct", "alt fuel"
    ]
    is_europe_source = any(s in source.lower() for s in europe_sources)
    
    mhcv_matches = sum(1 for keyword in EUROP_MHCV_KEYWORDS if keyword in full_text)
    lv_matches = sum(1 for keyword in GLOBAL_LV_KEYWORDS if keyword in full_text)
    
    if mhcv_matches >= 2:
        return "europe_mhcv"
    elif is_europe_source and mhcv_matches >= 1:
        return "europe_mhcv"
    elif is_europe_source:
        return "europe_other"
    else:
        return "global"


def categorize_articles(articles: List[Dict]) -> Dict[str, List[Dict]]:
    """Categorize list of articles"""
    categorized = {
        "europe_mhcv": [],
        "europe_other": [],
        "global": []
    }
    
    for article in articles:
        category = categorize_article(
            article.get("title", ""),
            article.get("description", ""),
            article.get("source", "")
        )
        article["category"] = category
        categorized[category].append(article)
    
    logger.info(
        f"📊 Categorized: {len(categorized['europe_mhcv'])} europe_mhcv, "
        f"{len(categorized['europe_other'])} europe_other, "
        f"{len(categorized['global'])} global"
    )
    
    return categorized
