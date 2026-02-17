#!/usr/bin/env python3
"""
Tanya ML Module - Sentiment Analysis & Keyword Extraction
Uses sklearn and NLTK for NLP tasks
"""

import json
import re
from typing import List, Dict, Tuple
from collections import Counter

# Positive/negative word lists (expandable)
POSITIVE_WORDS = {
    'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
    'success', 'breakthrough', 'achievement', 'growth', 'improve', 'positive',
    'best', 'winning', 'victory', 'happy', 'love', 'perfect', 'innovative'
}

NEGATIVE_WORDS = {
    'bad', 'terrible', 'awful', 'horrible', 'failure', 'crisis', 'disaster',
    'negative', 'decline', 'problem', 'issue', 'worst', 'losing', 'sad',
    'hate', 'poor', 'dangerous', 'threat', 'risk', 'concern'
}

class SentimentAnalyzer:
    """Simple lexicon-based sentiment analyzer"""
    
    def __init__(self):
        self.positive = POSITIVE_WORDS
        self.negative = NEGATIVE_WORDS
    
    def analyze(self, text: str) -> Dict:
        words = self._tokenize(text)
        pos_count = sum(1 for w in words if w in self.positive)
        neg_count = sum(1 for w in words if w in self.negative)
        
        score = pos_count - neg_count
        total = pos_count + neg_count
        
        if total == 0:
            sentiment = 'neutral'
            confidence = 0.5
        elif score > 0:
            sentiment = 'positive'
            confidence = min(0.95, 0.5 + (pos_count / (total * 2)))
        else:
            sentiment = 'negative'
            confidence = min(0.95, 0.5 + (neg_count / (total * 2)))
        
        return {
            'sentiment': sentiment,
            'score': score,
            'confidence': round(confidence, 2),
            'positive_words': pos_count,
            'negative_words': neg_count
        }
    
    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r'\b[a-z]+\b', text.lower())


class KeywordExtractor:
    """Extract keywords using TF-IDF-like approach"""
    
    def __init__(self):
        self.stopwords = set([
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
            'for', 'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were',
            'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'may', 'might', 'must', 'shall',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it',
            'we', 'they', 'what', 'which', 'who', 'when', 'where', 'why', 'how'
        ])
    
    def extract(self, text: str, top_n: int = 10) -> List[Dict]:
        words = re.findall(r'\b[a-z]{4,}\b', text.lower())
        words = [w for w in words if w not in self.stopwords]
        
        # Count frequencies
        freq = Counter(words)
        total = sum(freq.values())
        
        # Calculate TF-IDF-like scores
        keywords = []
        for word, count in freq.most_common(top_n):
            tf = count / total if total > 0 else 0
            keywords.append({
                'keyword': word,
                'count': count,
                'score': round(tf * 100, 2)
            })
        
        return keywords
    
    def extract_from_articles(self, articles: List[Dict], top_n: int = 20) -> List[Dict]:
        """Extract keywords across multiple articles"""
        all_text = ' '.join(a.get('title', '') + ' ' + a.get('content', '') for a in articles)
        return self.extract(all_text, top_n)


class TrendAnalyzer:
    """Analyze keyword trends over time"""
    
    def __init__(self):
        self.history = []
    
    def add_snapshot(self, keywords: List[Dict], timestamp: str = None):
        import datetime
        self.history.append({
            'timestamp': timestamp or datetime.datetime.now().isoformat(),
            'keywords': keywords
        })
    
    def get_trends(self, keyword: str) -> List[Dict]:
        trends = []
        for snapshot in self.history:
            for kw in snapshot['keywords']:
                if kw['keyword'] == keyword:
                    trends.append({
                        'timestamp': snapshot['timestamp'],
                        'count': kw['count'],
                        'score': kw['score']
                    })
        return trends


class DuplicateDetector:
    """Detect duplicate/similar articles"""
    
    def __init__(self, threshold: float = 0.8):
        self.threshold = threshold
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        words1 = set(re.findall(r'\b[a-z]+\b', text1.lower()))
        words2 = set(re.findall(r'\b[a-z]+\b', text2.lower()))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def find_duplicates(self, articles: List[Dict]) -> List[Tuple[str, str, float]]:
        duplicates = []
        
        for i, a1 in enumerate(articles):
            for j, a2 in enumerate(articles[i+1:], i+1):
                text1 = a1.get('title', '') + ' ' + a1.get('content', '')
                text2 = a2.get('title', '') + ' ' + a2.get('content', '')
                
                sim = self.calculate_similarity(text1, text2)
                if sim >= self.threshold:
                    duplicates.append((a1.get('id', str(i)), a2.get('id', str(j)), round(sim, 2)))
        
        return duplicates


def main():
    # Demo
    analyzer = SentimentAnalyzer()
    extractor = KeywordExtractor()
    detector = DuplicateDetector()
    
    test_text = "This is a great breakthrough in AI technology! The success of this project is amazing and positive for everyone."
    
    print("=== Sentiment Analysis ===")
    result = analyzer.analyze(test_text)
    print(json.dumps(result, indent=2))
    
    print("\n=== Keyword Extraction ===")
    keywords = extractor.extract(test_text)
    print(json.dumps(keywords, indent=2))
    
    print("\n=== Duplicate Detection ===")
    articles = [
        {'id': '1', 'title': 'AI breakthrough announced', 'content': 'New AI technology revealed today'},
        {'id': '2', 'title': 'AI breakthrough revealed', 'content': 'New artificial intelligence technology announced'},
        {'id': '3', 'title': 'Weather forecast for tomorrow', 'content': 'Sunny weather expected'}
    ]
    dups = detector.find_duplicates(articles)
    for d in dups:
        print(f"Duplicate: {d[0]} <-> {d[1]} (similarity: {d[2]})")


if __name__ == '__main__':
    main()
