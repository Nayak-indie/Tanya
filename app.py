"""
Tanya - Trending And New Yielded Articles
A polyglot news aggregator

Core functionality:
- RSS Fetcher: Rust
- Search: Rust
- Storage: Rust
- Dedup: Rust + C++
- Background Worker: Go
- REST API: Java
- Web Scraper: Node.js

Python only handles the UI (Streamlit)
"""
import streamlit as st
import subprocess
import json
import os
import pandas as pd
from datetime import datetime
import time

# Paths
RUST_BIN = "../rust/target/release"
CPP_BIN = "../cpp/bin"
JS_BIN = "js/src"
DATA_FILE = "data/news.json"

# Page Config
st.set_page_config(
    page_title="Tanya",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# Custom CSS
dark_css = """
<style>
    .stApp { background: #0e1117; color: #fafafa; }
    [data-testid="stSidebar"] { background: #161b22; }
    .news-card { background: #21262d; padding: 16px; border-radius: 8px; margin-bottom: 12px; border: 1px solid #30363d; }
    .headline { font-size: 18px; font-weight: 600; color: #58a6ff; }
    .source-tag { background: #238636; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px; }
    .time-tag { color: #8b949e; font-size: 12px; }
    .stat-number { font-size: 32px; font-weight: bold; color: #58a6ff; }
    .stat-label { font-size: 14px; color: #8b949e; }
    .sentiment-pos { background: #1a4731; color: #3fb950; padding: 4px 12px; border-radius: 20px; }
    .sentiment-neg { background: #4a1515; color: #f85149; padding: 4px 12px; border-radius: 20px; }
    .sentiment-neu { background: #30363d; color: #8b949e; padding: 4px 12px; border-radius: 20px; }
    .lang-badge { background: #1f6feb; color: white; padding: 2px 6px; border-radius: 4px; font-size: 10px; margin-left: 8px; }
</style>
"""

light_css = """
<style>
    .stApp { background: #ffffff; color: #1a1a1a; }
    [data-testid="stSidebar"] { background: #f5f5f5; }
    .news-card { background: #f9f9f9; padding: 16px; border-radius: 8px; margin-bottom: 12px; border: 1px solid #e0e0e0; }
    .headline { font-size: 18px; font-weight: 600; color: #2563eb; }
    .source-tag { background: #10b981; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px; }
    .time-tag { color: #6b7280; font-size: 12px; }
    .stat-number { font-size: 32px; font-weight: bold; color: #2563eb; }
    .stat-label { font-size: 14px; color: #6b7280; }
    .sentiment-pos { background: #d1fae5; color: #065f46; padding: 4px 12px; border-radius: 20px; }
    .sentiment-neg { background: #fee2e2; color: #991b1b; padding: 4px 12px; border-radius: 20px; }
    .sentiment-neu { background: #f3f4f6; color: #6b7280; padding: 4px 12px; border-radius: 20px; }
    .lang-badge { background: #3b82f6; color: white; padding: 2px 6px; border-radius: 4px; font-size: 10px; margin-left: 8px; }
</style>
"""

st.markdown(dark_css if st.session_state.theme == "dark" else light_css, unsafe_allow_html=True)

# === RUST FUNCTIONS ===
def run_rust(binary, args=[]):
    """Run Rust binary"""
    try:
        result = subprocess.run(
            [f"{RUST_BIN}/{binary}"] + args,
            capture_output=True,
            text=True,
            timeout=30,
            cwd="."
        )
        return result.stdout
    except FileNotFoundError:
        return None
    except Exception as e:
        return None

def fetch_news_rust():
    """Fetch news using Rust RSS fetcher"""
    output = run_rust("rss_fetcher")
    if output:
        lines = output.strip().split("\n")
        items = []
        for line in lines:
            if line.startswith("{"):
                try:
                    items.append(json.loads(line))
                except:
                    pass
        return items
    return []

def search_rust(query, limit=20):
    """Search using Rust engine"""
    output = run_rust("search", [query, "--limit", str(limit)])
    # Parse search results
    results = []
    if output:
        lines = output.strip().split("\n")
        for line in lines:
            if line.startswith("1.") or line.startswith("2."):
                results.append(line)
    return results

# === NODE.JS FUNCTIONS ===
def run_node(script, args=[]):
    """Run Node.js script"""
    try:
        result = subprocess.run(
            ["node", f"{JS_BIN}/{script}"] + args,
            capture_output=True,
            text=True,
            timeout=30,
            cwd="."
        )
        return result.stdout
    except FileNotFoundError:
        return None
    except Exception as e:
        return None

def fetch_news_node():
    """Fetch news using Node.js scraper"""
    output = run_node("scraper.js")
    return output

# === C++ FUNCTIONS ===
def run_cpp(binary, args=[]):
    """Run C++ binary"""
    try:
        result = subprocess.run(
            [f"{CPP_BIN}/{binary}"] + args,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout
    except FileNotFoundError:
        return None
    except Exception as e:
        return None

def dedup_cpp():
    """Run C++ duplicate detector"""
    output = run_cpp("dedup", ["stats"])
    return output

# === LOAD DATA ===
def load_news():
    """Load news from JSON file"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return []

def save_news(news):
    """Save news to JSON"""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(news, f, indent=2)
    except:
        pass

# === UI ===
st.title("📰 Tanya")
st.caption("Tanya (Trending And New Yielded Articles) - Polyglot News Aggregator")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Theme toggle
    if st.button("🌙 Toggle Theme"):
        st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
        st.rerun()
    
    st.divider()
    
    # Fetch options
    st.subheader("📥 Fetch News")
    
    fetcher = st.selectbox("Engine", ["Rust", "Node.js", "Python (fallback)"])
    
    if st.button("Fetch Now"):
        with st.spinner(f"Fetching with {fetcher}..."):
            if fetcher == "Rust":
                news = fetch_news_rust()
            elif fetcher == "Node.js":
                fetch_news_node()
                news = load_news()
            else:
                # Python fallback
                from collect.rss_scraper import RSSScraper
                scraper = RSSScraper()
                news = scraper.fetch_all()
                save_news(news)
        
        st.success(f"Fetched {len(news)} articles!")
    
    st.divider()
    
    # Stats
    st.subheader("📊 Stats")
    news = load_news()
    st.metric("Articles", len(news))
    
    # Dedup
    if st.button("🔄 Run Dedup (C++)"):
        output = dedup_cpp()
        if output:
            st.text(output)
        else:
            st.info("C++ not built - using Python fallback")
    
    st.divider()
    
    # Languages
    st.subheader("🌍 Languages")
    st.markdown("""
    - **Rust** <span class="lang-badge">RSS, Search, Storage</span>
    - **C++** <span class="lang-badge">Dedup</span>
    - **Go** <span class="lang-badge">Worker</span>
    - **Java** <span class="lang-badge">API</span>
    - **Node.js** <span class="lang-badge">Scraper</span>
    - **Python** <span class="lang-badge">UI Only</span>
    """, unsafe_allow_html=True)

# Main content
tab1, tab2, tab3 = st.tabs(["📰 News", "🔍 Search", "⭐ Favorites"])

with tab1:
    news = load_news()
    
    if not news:
        st.info("No news yet. Click 'Fetch News' in the sidebar!")
    else:
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            category = st.selectbox("Category", ["All"] + list(set(n.get("category", "General") for n in news)))
        with col2:
            sentiment = st.selectbox("Sentiment", ["All", "positive", "neutral", "negative"])
        with col3:
            source = st.selectbox("Source", ["All"] + list(set(n.get("source", "Unknown") for n in news)))
        
        # Filter
        filtered = news
        if category != "All":
            filtered = [n for n in filtered if n.get("category") == category]
        if sentiment != "All":
            filtered = [n for n in filtered if n.get("sentiment") == sentiment]
        if source != "All":
            filtered = [n for n in filtered if n.get("source") == source]
        
        # Display
        for item in filtered[:50]:
            with st.container():
                st.markdown(f"""
                <div class="news-card">
                    <a class="headline" href="{item.get('link', '#')}">{item.get('title', 'No title')}</a>
                    <div style="margin-top: 8px;">
                        <span class="source-tag">{item.get('source', 'Unknown')}</span>
                        <span class="time-tag">{item.get('category', 'General')}</span>
                        <span class="time-tag">• {item.get('reading_time', 1)} min read</span>
                    </div>
                    <p style="color: #8b949e; font-size: 14px; margin-top: 8px;">
                        {item.get('description', '')[:200]}...
                    </p>
                </div>
                """, unsafe_allow_html=True)

with tab2:
    query = st.text_input("🔍 Search", placeholder="Enter search term...")
    
    if query:
        with st.spinner("Searching with Rust..."):
            results = search_rust(query)
        
        if results:
            for r in results:
                st.text(r)
        else:
            # Fallback to simple filter
            news = load_news()
            results = [n for n in news if query.lower() in n.get("title", "").lower()]
            st.write(f"Found {len(results)} results")
            for r in results[:10]:
                st.write(f"- {r.get('title')}")

with tab3:
    st.info("Favorites coming soon!")
