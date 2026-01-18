"""
News MCP - Google News RSS Integration (No API Key Required)

This module provides MCP tools for fetching news from Google News RSS feeds.
Uses public Google News RSS which requires NO API key.

Tools:
- get_top_headlines: Get top news headlines by category/country
- search_news: Search for news articles by keyword/topic
- get_news_sources: Get list of news source recommendations

Note: Uses Google News RSS feeds - completely free, no API key needed.
"""

import json
import logging
import httpx
import re
import urllib.parse
from datetime import datetime
from langchain_core.tools import tool

logger = logging.getLogger(__name__)

# User-Agent header
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# Google News RSS base URL
GOOGLE_NEWS_RSS_BASE = "https://news.google.com/rss"

# Google News topic codes (these are the actual encoded topic IDs)
TOPIC_CODES = {
    "technology": "CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB",
    "business": "CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB",
    "sports": "CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FtVnVHZ0pWVXlnQVAB",
    "science": "CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp0Y1RjU0FtVnVHZ0pWVXlnQVAB",
    "health": "CAAqIQgKIhtDQkFTRGdvSUwyMHZNR3QwTlRFU0FtVnVLQUFQAQ",
    "entertainment": "CAAqJggKIiBDQkFTRWdvSUwyMHZNREpxYW5RU0FtVnVHZ0pWVXlnQVAB",
    "world": "CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB",
    "nation": "CAAqIggKIhxDQkFTRHdvSkwyMHZNRGxqTjNjd0VnSmxiaWdBUAE",
}


def _parse_rss_items(xml_text: str, max_items: int = 5) -> list:
    """Parse RSS XML and extract news items."""
    items = []
    
    # Find all items in RSS
    item_matches = re.findall(r'<item>(.*?)</item>', xml_text, re.DOTALL)
    
    for item_xml in item_matches[:max_items]:
        title_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>|<title>(.*?)</title>', item_xml)
        link_match = re.search(r'<link>(.*?)</link>', item_xml)
        pub_date_match = re.search(r'<pubDate>(.*?)</pubDate>', item_xml)
        source_match = re.search(r'<source.*?>(.*?)</source>', item_xml)
        
        title = ""
        if title_match:
            title = title_match.group(1) or title_match.group(2) or ""
            # Clean up HTML entities
            title = title.replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
        
        link = link_match.group(1) if link_match else ""
        pub_date = pub_date_match.group(1) if pub_date_match else ""
        source = source_match.group(1) if source_match else "Google News"
        
        if title:
            # Format the publication date
            try:
                dt = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %Z")
                formatted_date = dt.strftime("%Y-%m-%d %H:%M")
            except:
                formatted_date = pub_date[:16] if pub_date else "N/A"
            
            items.append({
                "title": title,
                "source": source,
                "published": formatted_date,
                "url": link
            })
    
    return items


@tool
def get_top_headlines(
    category: str = "general",
    country: str = "US",
    max_results: int = 5
) -> str:
    """
    Get top news headlines by category and country (FREE, no API key - uses Google News RSS).
    
    Args:
        category: News category - "general", "world", "business", "technology", 
                  "entertainment", "sports", "science", "health"
        country: Country code - "US", "GB", "IN", "AU", "CA" (default: "US")
        max_results: Number of articles to return (1-10, default: 5)
    
    Returns:
        Top news headlines with titles, sources, and publication times
    """
    try:
        category_lower = category.lower()
        
        # Build URL based on category
        if category_lower == "general" or category_lower not in TOPIC_CODES:
            # For general news, use the base RSS feed
            url = GOOGLE_NEWS_RSS_BASE
        else:
            # Use the topic code for specific categories
            topic_code = TOPIC_CODES[category_lower]
            url = f"{GOOGLE_NEWS_RSS_BASE}/topics/{topic_code}"
        
        # Add language/country parameters
        params = {"hl": "en", "gl": country.upper(), "ceid": f"{country.upper()}:en"}
        
        response = httpx.get(url, params=params, headers=HEADERS, timeout=10.0, follow_redirects=True)
        
        if response.status_code == 200:
            items = _parse_rss_items(response.text, min(max_results, 10))
            
            return json.dumps({
                "category": category,
                "country": country.upper(),
                "source": "Google News RSS (Free, No API Key)",
                "article_count": len(items),
                "articles": items
            }, indent=2)
        else:
            return f"Error: Unable to fetch headlines (status: {response.status_code})"
    except Exception as e:
        logger.error(f"Top headlines error: {e}")
        return f"Error fetching headlines: {str(e)}"


@tool
def search_news(
    query: str,
    max_results: int = 5
) -> str:
    """
    Search for news articles by keyword or topic (FREE, no API key - uses Google News RSS).
    
    Args:
        query: Search query/keywords (e.g., "artificial intelligence", "Tesla", "climate change")
        max_results: Number of articles to return (1-10, default: 5)
    
    Returns:
        News articles matching the search query
    """
    try:
        url = f"{GOOGLE_NEWS_RSS_BASE}/search"
        params = {"q": query, "hl": "en", "gl": "US", "ceid": "US:en"}
        
        response = httpx.get(url, params=params, headers=HEADERS, timeout=10.0, follow_redirects=True)
        
        if response.status_code == 200:
            items = _parse_rss_items(response.text, min(max_results, 10))
            
            return json.dumps({
                "query": query,
                "source": "Google News RSS (Free, No API Key)",
                "article_count": len(items),
                "articles": items
            }, indent=2)
        else:
            return f"Error: Unable to search news (status: {response.status_code})"
    except Exception as e:
        logger.error(f"News search error: {e}")
        return f"Error searching news: {str(e)}"


@tool
def get_news_sources(category: str = "general") -> str:
    """
    Get recommended news sources for a category.
    
    Args:
        category: News category - "general", "business", "technology", 
                  "entertainment", "sports", "science", "health"
    
    Returns:
        List of recommended news sources
    """
    # Pre-defined list of major news sources by category (no API needed)
    sources = {
        "general": [
            {"name": "Reuters", "url": "reuters.com", "description": "International news organization"},
            {"name": "Associated Press", "url": "apnews.com", "description": "American news agency"},
            {"name": "BBC News", "url": "bbc.com/news", "description": "British Broadcasting Corporation"},
            {"name": "CNN", "url": "cnn.com", "description": "Cable News Network"},
            {"name": "The Guardian", "url": "theguardian.com", "description": "British daily newspaper"},
            {"name": "NPR", "url": "npr.org", "description": "National Public Radio"}
        ],
        "business": [
            {"name": "Bloomberg", "url": "bloomberg.com", "description": "Financial news and data"},
            {"name": "CNBC", "url": "cnbc.com", "description": "Business news channel"},
            {"name": "Financial Times", "url": "ft.com", "description": "British business newspaper"},
            {"name": "Wall Street Journal", "url": "wsj.com", "description": "American business newspaper"},
            {"name": "Forbes", "url": "forbes.com", "description": "Business magazine"}
        ],
        "technology": [
            {"name": "TechCrunch", "url": "techcrunch.com", "description": "Technology news"},
            {"name": "The Verge", "url": "theverge.com", "description": "Technology news and media"},
            {"name": "Wired", "url": "wired.com", "description": "Technology magazine"},
            {"name": "Ars Technica", "url": "arstechnica.com", "description": "Technology news site"},
            {"name": "Engadget", "url": "engadget.com", "description": "Technology blog"}
        ],
        "entertainment": [
            {"name": "Entertainment Weekly", "url": "ew.com", "description": "Entertainment magazine"},
            {"name": "Variety", "url": "variety.com", "description": "Entertainment trade publication"},
            {"name": "Hollywood Reporter", "url": "hollywoodreporter.com", "description": "Entertainment news"},
            {"name": "Rolling Stone", "url": "rollingstone.com", "description": "Music and culture magazine"}
        ],
        "sports": [
            {"name": "ESPN", "url": "espn.com", "description": "Sports news network"},
            {"name": "BBC Sport", "url": "bbc.com/sport", "description": "Sports news from BBC"},
            {"name": "Sports Illustrated", "url": "si.com", "description": "Sports magazine"},
            {"name": "Bleacher Report", "url": "bleacherreport.com", "description": "Sports news"}
        ],
        "science": [
            {"name": "Nature", "url": "nature.com", "description": "Scientific journal"},
            {"name": "Science", "url": "science.org", "description": "Scientific journal"},
            {"name": "New Scientist", "url": "newscientist.com", "description": "Science magazine"},
            {"name": "Scientific American", "url": "scientificamerican.com", "description": "Science magazine"}
        ],
        "health": [
            {"name": "WebMD", "url": "webmd.com", "description": "Health information"},
            {"name": "Healthline", "url": "healthline.com", "description": "Health news"},
            {"name": "Medical News Today", "url": "medicalnewstoday.com", "description": "Medical news"},
            {"name": "Mayo Clinic", "url": "mayoclinic.org", "description": "Medical information"}
        ]
    }
    
    category_sources = sources.get(category.lower(), sources["general"])
    
    return json.dumps({
        "category": category,
        "note": "These are recommended sources. Use search_news() to find specific articles.",
        "sources": category_sources
    }, indent=2)


# Export all news tools
NEWS_TOOLS = [
    get_top_headlines,
    search_news,
    get_news_sources
]
