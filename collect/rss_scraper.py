"""
RSS Feed Scraper - Collects news from RSS sources
"""
import feedparser
import requests
from datetime import datetime
from typing import List, Dict, Optional
import json
import os

RSS_SOURCES_FILE = "data/sources.json"
NEWS_DATA_FILE = "data/news.json"

class RSSScraper:
    def __init__(self):
        self.sources = self.load_sources()
    
    def load_sources(self) -> List[Dict]:
        """Load configured RSS sources"""
        os.makedirs("data", exist_ok=True)
        if os.path.exists(RSS_SOURCES_FILE):
            with open(RSS_SOURCES_FILE, "r") as f:
                return json.load(f)
        # Default sources - Comprehensive news coverage
        defaults = [
            # Major News
            {"name": "BBC News", "url": "https://feeds.bbci.co.uk/news/rss.xml", "enabled": True, "category": "World"},
            {"name": "Reuters World", "url": "https://www.reutersagency.com/feed/?best-regions=europe&post_type=best", "enabled": True, "category": "World"},
            {"name": "CNN", "url": "http://rss.cnn.com/rss/edition.rss", "enabled": False, "category": "World"},
            {"name": "Al Jazeera", "url": "https://www.aljazeera.com/xml/rss/all.xml", "enabled": False, "category": "World"},
            
            # Tech
            {"name": "TechCrunch", "url": "https://techcrunch.com/feed/", "enabled": True, "category": "Tech"},
            {"name": "Hacker News", "url": "https://news.ycombinator.com/rss", "enabled": True, "category": "Tech"},
            {"name": "Wired", "url": "https://www.wired.com/feed/rss", "enabled": False, "category": "Tech"},
            {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml", "enabled": False, "category": "Tech"},
            {"name": "Ars Technica", "url": "https://feeds.arstechnica.com/arstechnica/index", "enabled": False, "category": "Tech"},
            
            # Science
            {"name": "NASA", "url": "https://www.nasa.gov/rss/dyn/breaking_news.rss", "enabled": False, "category": "Science"},
            {"name": "Science Daily", "url": "https://www.sciencedaily.com/rss/all.xml", "enabled": False, "category": "Science"},
            {"name": "Nature", "url": "https://www.nature.com/nature.rss", "enabled": False, "category": "Science"},
            
            # Business/Finance
            {"name": "Bloomberg", "url": "https://feeds.bloomberg.com/markets/news.rss", "enabled": False, "category": "Finance"},
            {"name": "CNBC", "url": "https://www.cnbc.com/id/100003114/device/rss/rss.html", "enabled": False, "category": "Finance"},
            {"name": "Financial Times", "url": "https://www.ft.com/rss/home", "enabled": False, "category": "Finance"},
            
            # AI & ML
            {"name": "MIT Tech Review", "url": "https://www.technologyreview.com/feed/", "enabled": False, "category": "AI"},
            {"name": "OpenAI Blog", "url": "https://openai.com/blog/rss.xml", "enabled": False, "category": "AI"},
            
            # Security
            {"name": "Krebs on Security", "url": "https://krebsonsecurity.com/feed/", "enabled": False, "category": "Security"},
            {"name": "Bleeping Computer", "url": "https://www.bleepingcomputer.com/feed/", "enabled": False, "category": "Security"},
            
            # Entertainment
            {"name": " Variety", "url": "https://variety.com/feed/", "enabled": False, "category": "Entertainment"},
            {"name": "IGN", "url": "https://feeds.feedburner.com/ign/all", "enabled": False, "category": "Gaming"},
        ]
        self.save_sources(defaults)
        return defaults
    
    def save_sources(self, sources: List[Dict]):
        """Save sources to file"""
        os.makedirs("data", exist_ok=True)
        with open(RSS_SOURCES_FILE, "w") as f:
            json.dump(sources, f, indent=2)
        self.sources = sources
    
    def fetch_feed(self, url: str) -> Optional[Dict]:
        """Fetch and parse an RSS feed"""
        try:
            feed = feedparser.parse(url)
            return {
                "title": feed.feed.get("title", "Unknown"),
                "entries": [
                    {
                        "title": entry.get("title", "No Title"),
                        "link": entry.get("link", ""),
                        "published": entry.get("published", ""),
                        "summary": entry.get("summary", "")[:200],
                        "source": feed.feed.get("title", "Unknown")
                    }
                    for entry in feed.entries[:20]
                ]
            }
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def collect_all(self) -> List[Dict]:
        """Collect news from all enabled sources"""
        all_news = []
        for source in self.sources:
            if source.get("enabled", True):
                result = self.fetch_feed(source["url"])
                if result and result.get("entries"):
                    all_news.extend(result["entries"])
        
        # Sort by published date (newest first)
        all_news.sort(key=lambda x: x.get("published", ""), reverse=True)
        
        # Save to file
        os.makedirs("data", exist_ok=True)
        with open(NEWS_DATA_FILE, "w") as f:
            json.dump(all_news, f, indent=2)
        
        return all_news
    
    def add_source(self, name: str, url: str):
        """Add a new RSS source"""
        new_source = {"name": name, "url": url, "enabled": True}
        self.sources.append(new_source)
        self.save_sources(self.sources)
    
    def remove_source(self, name: str):
        """Remove a source by name"""
        self.sources = [s for s in self.sources if s["name"] != name]
        self.save_sources(self.sources)
    
    def toggle_source(self, name: str):
        """Toggle source enabled/disabled"""
        for s in self.sources:
            if s["name"] == name:
                s["enabled"] = not s.get("enabled", True)
        self.save_sources(self.sources)
    
    def get_sources_by_category(self) -> Dict[str, List[Dict]]:
        """Get sources grouped by category"""
        categories = {}
        for s in self.sources:
            cat = s.get("category", "Other")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(s)
        return categories
    
    def get_enabled_count(self) -> int:
        """Get count of enabled sources"""
        return sum(1 for s in self.sources if s.get("enabled", True))
    
    def test_feed(self, url: str) -> bool:
        """Test if a feed URL is valid"""
        try:
            feed = feedparser.parse(url)
            return len(feed.entries) > 0 if feed.entries else False
        except:
            return False

if __name__ == "__main__":
    scraper = RSSScraper()
    news = scraper.collect_all()
    print(f"Collected {len(news)} articles")
