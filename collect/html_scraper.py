"""
HTML Page Scraper - Scrapes news from regular web pages
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional
import json
import os

HTML_SOURCES_FILE = "data/html_sources.json"

class HTMLScraper:
    def __init__(self):
        self.sources = self.load_sources()
    
    def load_sources(self) -> List[Dict]:
        """Load configured HTML sources"""
        os.makedirs("data", exist_ok=True)
        if os.path.exists(HTML_SOURCES_FILE):
            with open(HTML_SOURCES_FILE, "r") as f:
                return json.load(f)
        # Default sources
        defaults = [
            {"name": "BBC Home", "url": "https://www.bbc.com/news", "enabled": True},
            {"name": "CNN", "url": "https://www.cnn.com", "enabled": False},
        ]
        self.save_sources(defaults)
        return defaults
    
    def save_sources(self, sources: List[Dict]):
        """Save sources to file"""
        os.makedirs("data", exist_ok=True)
        with open(HTML_SOURCES_FILE, "w") as f:
            json.dump(sources, f, indent=2)
        self.sources = sources
    
    def fetch_page(self, url: str) -> Optional[Dict]:
        """Fetch and parse an HTML page for news"""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Try to find article titles (generic approach)
            articles = []
            
            # Look for common news article selectors
            selectors = [
                "article h2", "article h3", 
                ".headline", ".news-title",
                "a[href*='/news/']", "a[href*='/article/']"
            ]
            
            for selector in selectors:
                elements = soup.select(selector)
                for el in elements[:10]:
                    title = el.get_text(strip=True)
                    link = ""
                    if el.name == "a":
                        link = el.get("href", "")
                    else:
                        parent = el.find_parent("a")
                        if parent:
                            link = parent.get("href", "")
                    
                    if title and len(title) > 10:
                        articles.append({
                            "title": title,
                            "link": link if link.startswith("http") else url + link,
                            "source": url.split("//")[1].split("/")[0] if "//" in url else url
                        })
            
            return {
                "url": url,
                "articles": articles[:20]
            }
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def collect_all(self) -> List[Dict]:
        """Collect news from all enabled HTML sources"""
        all_news = []
        for source in self.sources:
            if source.get("enabled", True):
                result = self.fetch_page(source["url"])
                if result and result.get("articles"):
                    for article in result["articles"]:
                        article["source"] = source["name"]
                        all_news.append(article)
        return all_news
    
    def add_source(self, name: str, url: str):
        """Add a new HTML source"""
        new_source = {"name": name, "url": url, "enabled": True}
        self.sources.append(new_source)
        self.save_sources(self.sources)
    
    def remove_source(self, name: str):
        """Remove a source by name"""
        self.sources = [s for s in self.sources if s["name"] != name]
        self.save_sources(self.sources)

if __name__ == "__main__":
    scraper = HTMLScraper()
    news = scraper.collect_all()
    print(f"Collected {len(news)} articles from HTML sources")
