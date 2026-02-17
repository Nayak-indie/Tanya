"""
Storage Module - Handles data persistence for collected news
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

DATA_DIR = "data"
NEWS_FILE = os.path.join(DATA_DIR, "news.json")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")

class NewsStorage:
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
    
    def save_news(self, news: List[Dict]):
        """Save news to file with timestamp"""
        data = {
            "collected_at": datetime.now().isoformat(),
            "articles": news
        }
        with open(NEWS_FILE, "w") as f:
            json.dump(data, f, indent=2)
    
    def load_news(self) -> List[Dict]:
        """Load saved news"""
        if os.path.exists(NEWS_FILE):
            with open(NEWS_FILE, "r") as f:
                data = json.load(f)
                # Handle both dict and list formats
                if isinstance(data, list):
                    return data
                return data.get("articles", [])
        return []
    
    def get_last_collection_time(self) -> Optional[str]:
        """Get timestamp of last collection"""
        if os.path.exists(NEWS_FILE):
            with open(NEWS_FILE, "r") as f:
                data = json.load(f)
                # Handle both dict and list formats
                if isinstance(data, list):
                    return None
                return data.get("collected_at")
        return None
    
    def add_to_history(self, article: Dict):
        """Add article to history"""
        history = self.load_history()
        # Check for duplicates
        if not any(a.get("link") == article.get("link") for a in history):
            history.insert(0, {
                **article,
                "saved_at": datetime.now().isoformat()
            })
            # Keep last 1000 articles
            history = history[:1000]
            with open(HISTORY_FILE, "w") as f:
                json.dump(history, f, indent=2)
    
    def load_history(self) -> List[Dict]:
        """Load article history"""
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        return []
    
    def clear_news(self):
        """Clear current news"""
        if os.path.exists(NEWS_FILE):
            os.remove(NEWS_FILE)
    
    def clear_history(self):
        """Clear history"""
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
