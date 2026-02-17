"""
NewsFlow - Web News Collector & Aggregator
A powerful news collection tool with modern Streamlit UI

Features:
- Full-text search (Rust engine ready)
- Sentiment analysis (Python ML)
- Keyword extraction
- Duplicate detection (C++ engine ready)
- Export to CSV/JSON
- Favorites/bookmarks
- Reading time estimates
- Theme toggle (dark/light)
- REST API ready (Java server)
"""
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import time
import re

# Import collectors
from collect.rss_scraper import RSSScraper
from collect.html_scraper import HTMLScraper
from collect.storage import NewsStorage

# Import ML features
try:
    from backend.ml.analyzer import SentimentAnalyzer, KeywordExtractor, DuplicateDetector
    from backend.ml.kid_summarizer import StorySummarizer
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

# Page Config
st.set_page_config(
    page_title="NewsFlow",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme toggle
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

# Custom CSS for themes
dark_css = """
<style>
    .stApp { background: #0e1117; color: #fafafa; }
    [data-testid="stSidebar"] { background: #161b22; }
    .news-card { background: #21262d; padding: 16px; border-radius: 8px; margin-bottom: 12px; border: 1px solid #30363d; }
    .headline { font-size: 18px; font-weight: 600; color: #58a6ff; text-decoration: none; }
    .headline:hover { color: #79c0ff; }
    .source-tag { background: #238636; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px; margin-right: 8px; }
    .time-tag { color: #8b949e; font-size: 12px; }
    .stat-box { background: #21262d; padding: 16px; border-radius: 8px; text-align: center; border: 1px solid #30363d; }
    .stat-number { font-size: 32px; font-weight: bold; color: #58a6ff; }
    .stat-label { font-size: 14px; color: #8b949e; }
    .sentiment-pos { background: #1a4731; color: #3fb950; padding: 4px 12px; border-radius: 20px; font-size: 12px; }
    .sentiment-neg { background: #4a1515; color: #f85149; padding: 4px 12px; border-radius: 20px; font-size: 12px; }
    .sentiment-neu { background: #30363d; color: #8b949e; padding: 4px 12px; border-radius: 20px; font-size: 12px; }
    .favorite-btn { background: none; border: none; font-size: 20px; cursor: pointer; }
</style>
"""

light_css = """
<style>
    .stApp { background: #ffffff; color: #1a1a1a; }
    [data-testid="stSidebar"] { background: #f5f5f5; }
    .news-card { background: #f9f9f9; padding: 16px; border-radius: 8px; margin-bottom: 12px; border: 1px solid #e0e0e0; }
    .headline { font-size: 18px; font-weight: 600; color: #2563eb; text-decoration: none; }
    .headline:hover { color: #1d4ed8; }
    .source-tag { background: #10b981; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px; margin-right: 8px; }
    .time-tag { color: #6b7280; font-size: 12px; }
    .stat-box { background: #f9f9f9; padding: 16px; border-radius: 8px; text-align: center; border: 1px solid #e0e0e0; }
    .stat-number { font-size: 32px; font-weight: bold; color: #2563eb; }
    .stat-label { font-size: 14px; color: #6b7280; }
    .sentiment-pos { background: #d1fae5; color: #065f46; padding: 4px 12px; border-radius: 20px; font-size: 12px; }
    .sentiment-neg { background: #fee2e2; color: #991b1b; padding: 4px 12px; border-radius: 20px; font-size: 12px; }
    .sentiment-neu { background: #f3f4f6; color: #6b7280; padding: 4px 12px; border-radius: 20px; font-size: 12px; }
    .favorite-btn { background: none; border: none; font-size: 20px; cursor: pointer; }
</style>
"""

st.markdown(dark_css if st.session_state.theme == "dark" else light_css, unsafe_allow_html=True)

# Initialize session state
if "rss_scraper" not in st.session_state:
    st.session_state.rss_scraper = RSSScraper()
if "html_scraper" not in st.session_state:
    st.session_state.html_scraper = HTMLScraper()
if "storage" not in st.session_state:
    st.session_state.storage = NewsStorage()
if "news" not in st.session_state:
    st.session_state.news = st.session_state.storage.load_news()
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = st.session_state.storage.get_last_collection_time()
if "favorites" not in st.session_state:
    st.session_state.favorites = set()
if "sentiment_cache" not in st.session_state:
    st.session_state.sentiment_cache = {}
if "story_summarizer" not in st.session_state and ML_AVAILABLE:
    st.session_state.story_summarizer = StorySummarizer()

# ML analyzers
if ML_AVAILABLE:
    sentiment_analyzer = SentimentAnalyzer()
    keyword_extractor = KeywordExtractor()
    duplicate_detector = DuplicateDetector()

def analyze_sentiment(text):
    """Get cached or fresh sentiment analysis"""
    cache_key = hash(text[:100])
    if cache_key not in st.session_state.sentiment_cache:
        result = sentiment_analyzer.analyze(text)
        st.session_state.sentiment_cache[cache_key] = result.get('sentiment', 'neutral')
    return st.session_state.sentiment_cache[cache_key]

def calculate_reading_time(text):
    """Estimate reading time (200 WPM)"""
    words = len(re.findall(r'\w+', text))
    return max(1, words // 200)

def export_to_json(articles, filepath="export.json"):
    """Export articles to JSON"""
    with open(filepath, 'w') as f:
        json.dump(articles, f, indent=2)
    return filepath

def export_to_csv(articles, filepath="export.csv"):
    """Export articles to CSV"""
    df = pd.DataFrame(articles)
    df.to_csv(filepath, index=False)
    return filepath

# Sidebar
with st.sidebar:
    st.title("📰 NewsFlow")
    
    # Theme toggle button
    theme_icon = "🌙" if st.session_state.theme == "dark" else "☀️"
    if st.button(f"{theme_icon} Toggle Theme"):
        toggle_theme()
        st.rerun()
    
    st.markdown("---")
    
    # Auto-refresh toggle
    auto_refresh = st.toggle("🔄 Auto-refresh (30s)", value=False)
    if auto_refresh:
        time.sleep(0.1)
        st.rerun()
    
    # Refresh button
    if st.button("🔃 Refresh Now"):
        with st.spinner("Collecting news..."):
            rss_news = st.session_state.rss_scraper.collect_all()
            html_news = st.session_state.html_scraper.collect_all()
            all_news = rss_news + html_news
            
            # Add ML features
            if ML_AVAILABLE:
                for article in all_news:
                    text = article.get('title', '') + ' ' + article.get('summary', '')
                    article['sentiment'] = analyze_sentiment(text)
                    article['reading_time'] = calculate_reading_time(text)
            
            st.session_state.news = all_news
            st.session_state.storage.save_news(all_news)
            st.session_state.last_refresh = datetime.now().isoformat()
        st.success(f"Collected {len(all_news)} articles!")
    
    st.markdown("---")
    
    # Stats
    st.subheader("📊 Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{len(st.session_state.news)}</div>
            <div class="stat-label">Articles</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{len(st.session_state.favorites)}</div>
            <div class="stat-label">Favorites</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Sentiment distribution
    if ML_AVAILABLE and st.session_state.news:
        sentiments = {}
        for a in st.session_state.news:
            s = a.get('sentiment', 'neutral')
            sentiments[s] = sentiments.get(s, 0) + 1
        st.markdown("**Sentiment:** " + " | ".join(f"{k}: {v}" for k, v in sentiments.items()))
    
    st.markdown("---")
    
    # 📖 Story Summary Panel
    st.markdown("### 📖 News Story Explained")
    st.markdown("*Full context + history + my take*")
    
    # Select article to explain
    if st.session_state.news:
        article_titles = [a.get('title', 'Untitled')[:50] for a in st.session_state.news]
        selected_idx = st.selectbox(
            "Pick a story:", 
            range(len(st.session_state.news)),
            format_func=lambda i: article_titles[i],
            key="story_select"
        )
        
        if st.button("📖 Get Full Story", key="story_btn"):
            article = st.session_state.news[selected_idx]
            story = st.session_state.story_summarizer.generate_full_story(
                article.get('title', ''),
                article.get('summary', '')
            )
            
            st.markdown("---")
            # Parse and display sections
            lines = story.split('\n')
            in_section = ""
            for line in lines:
                if line.startswith("## "):
                    in_section = line.replace("## ", "")
                    st.markdown(f"### {in_section}")
                elif line.startswith("# "):
                    st.markdown(f"# {line.replace('# ', '')}")
                elif line.startswith("*") and line.endswith("*"):
                    st.caption(line.strip("*"))
                elif line.strip():
                    st.markdown(line)
    else:
        st.caption("Collect some news first to see explanations!")
    
    st.markdown("---")
    
    # Export options
    with st.expander("💾 Export"):
        if st.button("Export JSON"):
            path = export_to_json(st.session_state.news)
            st.success(f"Exported to {path}")
        if st.button("Export CSV"):
            path = export_to_csv(st.session_state.news)
            st.success(f"Exported to {path}")
    
    # Last refresh time
    if st.session_state.last_refresh:
        st.caption(f"Last updated: {st.session_state.last_refresh[:19]}")

# Main content
st.title("📰 News Dashboard")

# Tab interface
tab1, tab2, tab3, tab4 = st.tabs(["📰 All News", "⭐ Favorites", "📡 RSS Sources", "🌐 HTML Sources"])

with tab1:
    if not st.session_state.news:
        st.info("No news collected yet. Click 'Refresh Now' in the sidebar!")
    else:
        # Search
        search = st.text_input("🔍 Search headlines...", placeholder="Type to filter...")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            sentiment_filter = st.selectbox("Sentiment", ["All", "positive", "neutral", "negative"])
        with col2:
            source_filter = st.selectbox("Source", ["All"] + list(set(a.get('source', 'Unknown') for a in st.session_state.news)))
        with col3:
            sort_by = st.selectbox("Sort by", ["Date", "Title"])
        
        # Filter news
        filtered_news = st.session_state.news
        if search:
            filtered_news = [n for n in filtered_news if search.lower() in n.get("title", "").lower()]
        if sentiment_filter != "All":
            filtered_news = [n for n in filtered_news if n.get("sentiment", "neutral") == sentiment_filter]
        if source_filter != "All":
            filtered_news = [n for n in filtered_news if n.get("source") == source_filter]
        
        if sort_by == "Title":
            filtered_news = sorted(filtered_news, key=lambda x: x.get("title", ""))
        
        st.markdown(f"**{len(filtered_news)} articles**")
        
        # Display news
        for i, article in enumerate(filtered_news):
            fav_icon = "⭐" if article.get('link') in st.session_state.favorites else "☆"
            
            sentiment = article.get('sentiment', 'neutral')
            sentiment_class = f"sentiment-{sentiment[:3]}"
            
            with st.container():
                col_info, col_fav, col_eli5 = st.columns([5, 1, 1])
                with col_fav:
                    if st.button(f"{fav_icon}", key=f"fav_{i}"):
                        link = article.get('link')
                        if link in st.session_state.favorites:
                            st.session_state.favorites.discard(link)
                        else:
                            st.session_state.favorites.add(link)
                        st.rerun()
                with col_eli5:
                    if st.button("📖", key=f"eli5_{i}"):
                        st.session_state.eli5_selected = i
                        st.rerun()
                
                with col_info:
                    st.markdown(f"""
                    <div class="news-card">
                        <a href="{article.get('link', '#')}" target="_blank" class="headline">{article.get('title', 'No Title')}</a>
                        <div style="margin-top: 8px;">
                            <span class="source-tag">{article.get('source', 'Unknown')}</span>
                            <span class="{sentiment_class}">{sentiment}</span>
                            <span class="time-tag">{article.get('reading_time', 5)} min read</span>
                            <span class="time-tag">{article.get('published', '')[:16]}</span>
                        </div>
                        <p style="color: #8b949e; font-size: 14px; margin-top: 8px;">{article.get('summary', '')[:150]}...</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Show ELI5 summary if selected
            if hasattr(st.session_state, 'eli5_selected') and st.session_state.eli5_selected == i:
                with st.expander("📖 Full Story Explained", expanded=True):
                    story = st.session_state.story_summarizer.generate_full_story(
                        article.get('title', ''),
                        article.get('summary', '')
                    )
                    
                    lines = story.split('\n')
                    for line in lines:
                        if line.startswith("## "):
                            st.markdown(f"**{line.replace('## ', '')}**")
                        elif line.startswith("### "):
                            st.markdown(f"**{line}**")
                        elif line.startswith("*") and line.endswith("*"):
                            st.caption(line.strip("*"))
                        elif line.strip():
                            st.markdown(line)

with tab2:
    st.subheader("⭐ Your Favorites")
    fav_articles = [a for a in st.session_state.news if a.get('link') in st.session_state.favorites]
    
    if not fav_articles:
        st.info("No favorites yet. Click ⭐ on articles to add them!")
    else:
        for article in fav_articles:
            sentiment = article.get('sentiment', 'neutral')
            st.markdown(f"""
            <div class="news-card">
                <a href="{article.get('link', '#')}" target="_blank" class="headline">{article.get('title', 'No Title')}</a>
                <div style="margin-top: 8px;">
                    <span class="source-tag">{article.get('source', 'Unknown')}</span>
                    <span class="time-tag">{article.get('published', '')[:16]}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab3:
    st.subheader("📡 RSS Feed Sources")
    
    # Quick stats
    enabled_count = st.session_state.rss_scraper.get_enabled_count()
    total_count = len(st.session_state.rss_scraper.sources)
    st.markdown(f"**{enabled_count}/{total_count} sources enabled**")
    
    # Add new source form
    with st.expander("➕ Add Custom RSS Source", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("Source Name", placeholder="e.g., My Tech News", key="rss_new_name")
        with col2:
            new_url = st.text_input("RSS Feed URL", placeholder="https://example.com/feed.xml", key="rss_new_url")
        
        # Suggest categories
        new_category = st.selectbox("Category", ["World", "Tech", "Science", "Finance", "AI", "Security", "Entertainment", "Other"], key="rss_new_cat")
        
        if st.button("➕ Add Source", key="add_rss_source"):
            if new_name and new_url:
                # Test the feed first
                with st.spinner("Testing feed..."):
                    is_valid = st.session_state.rss_scraper.test_feed(new_url)
                if is_valid:
                    st.session_state.rss_scraper.sources.append({
                        "name": new_name,
                        "url": new_url,
                        "enabled": True,
                        "category": new_category
                    })
                    st.session_state.rss_scraper.save_sources(st.session_state.rss_scraper.sources)
                    st.success(f"✅ Added '{new_name}'!")
                    st.rerun()
                else:
                    st.error("❌ Could not fetch feed. Please check the URL.")
            else:
                st.warning("Please enter both name and URL")
    
    # Quick enable/disable buttons
    st.markdown("### 🚀 Quick Toggle")
    col1, col2 = st.columns([3, 1])
    with col1:
        quick_toggle = st.selectbox("Select source to toggle", 
                                    [s["name"] for s in st.session_state.rss_scraper.sources],
                                    key="quick_toggle_src")
    with col2:
        if st.button("✅/❌ Toggle", key="toggle_quick"):
            st.session_state.rss_scraper.toggle_source(quick_toggle)
            st.rerun()
    
    st.markdown("---")
    
    # Sources by category
    sources_by_cat = st.session_state.rss_scraper.get_sources_by_category()
    
    for category, sources in sources_by_cat.items():
        with st.expander(f"📁 {category} ({len(sources)} sources)", expanded=True):
            # Enable all / Disable all buttons
            c1, c2 = st.columns([6, 2])
            with c1:
                st.markdown(f"**{len([s for s in sources if s.get('enabled')])} enabled**")
            with c2:
                if st.button(f"Enable All", key=f"enable_cat_{category}"):
                    for s in sources:
                        s["enabled"] = True
                    st.session_state.rss_scraper.save_sources(st.session_state.rss_scraper.sources)
                    st.rerun()
            
            # List sources
            for source in sources:
                col_name, col_status, col_del = st.columns([4, 1, 1])
                with col_name:
                    status_icon = "✅" if source.get("enabled") else "❌"
                    st.markdown(f"{status_icon} **{source['name']}**")
                    st.caption(source['url'][:60] + "..." if len(source['url']) > 60 else source['url'])
                with col_status:
                    toggle_label = "Disable" if source.get("enabled") else "Enable"
                    if st.button(f"{'🔴' if source.get('enabled') else '🟢'}", key=f"status_{source['name']}"):
                        st.session_state.rss_scraper.toggle_source(source['name'])
                        st.rerun()
                with col_del:
                    if st.button("🗑️", key=f"del_{source['name']}"):
                        st.session_state.rss_scraper.remove_source(source['name'])
                        st.rerun()
                st.divider()

with tab4:
    st.subheader("🌐 HTML Page Sources")
    
    with st.expander("➕ Add HTML Source"):
        new_name = st.text_input("Source Name", key="html_name")
        new_url = st.text_input("Page URL", key="html_url")
        if st.button("Add HTML Source"):
            if new_name and new_url:
                st.session_state.html_scraper.add_source(new_name, new_url)
                st.success(f"Added {new_name}!")
                st.rerun()
    
    for source in st.session_state.html_scraper.sources:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"**{source['name']}**")
            st.caption(source['url'][:50] + "...")
        with col2:
            if st.button(f"{'✅' if source.get('enabled', True) else '❌'}", key=f"html_{source['name']}"):
                st.session_state.html_scraper.toggle_source(source['name'])
                st.rerun()
        with col3:
            if st.button("🗑️", key=f"del_html_{source['name']}"):
                st.session_state.html_scraper.remove_source(source['name'])
                st.rerun()

# Footer
st.markdown("---")
st.caption("📰 NewsFlow - Built with Streamlit | Multi-language powered: Python, Rust, C++, Java, Go, JS, C#, Ruby, PHP, Perl, Fortran, R, SQL, Delphi | Data collected from RSS & HTML sources")
