# 📰 Tanya - Smart News Aggregator

<div align="center">

![Python](https://img.shields.io/badge/python-3.12+-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

</div>

---

Tanya (Trending And New Yielded Articles) is a polyglot news aggregator experiment—scraping, analyzing, and serving news using Python, Rust, C++, Java, Go, and more. Built with 14+ languages as a fun experiment in seeing how different technologies can work together to build something useful.

---

## ✨ Features

### 📊 News Collection
- **Multi-source RSS Aggregation** - Collect from 20+ pre-configured sources
- **HTML Scraping** - Extract news from any webpage
- **Auto-refresh** - Keep your feed up to date

### 🧠 Smart Analysis
- **Sentiment Analysis** - Understand the tone of each article
- **Keyword Extraction** - Discover trending topics
- **Duplicate Detection** - Filter out similar articles
- **Reading Time** - Know before you click

### 📖 Story Mode
- **Backstory** - How it all started with historical context
- **Current Events** - What's happening now
- **My Take** - Balanced perspective and opinion

### 🌍 Multi-Language Engine
| Language | Purpose |
|----------|---------|
| Python | ML, Streamlit UI |
| Rust | High-performance search |
| C++ | Core processing |
| Java | REST API |
| Go | Background workers |
| JavaScript | Frontend |
| C# | Notifications |
| Ruby | Newsletter |
| PHP | Webhooks |
| Perl | Text processing |
| Fortran | Statistics |
| R | Analytics |
| SQL | Database |
| Delphi | Desktop |

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/Nayak-indie/Tanya.git
cd Tanya

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Open [http://localhost:8502](http://localhost:8502) in your browser!

---

## 📁 Project Structure

```
Tanya/
├── app.py                    # Main Streamlit app
├── collect/                  # News collectors
│   ├── rss_scraper.py
│   ├── html_scraper.py
│   └── storage.py
├── backend/                  # Backend services
│   ├── ml/                  # ML modules
│   ├── api/                 # REST API (Java)
│   ├── workers/             # Background workers (Go)
│   └── database/            # SQL schemas
├── core/                    # Core engines
│   ├── cpp/                # C++ engine
│   ├── search/             # Rust search
│   └── text_processor.pl   # Perl processor
├── frontend/               # Frontend assets
│   ├── js/
│   └── css/
├── integrations/            # Integrations
│   ├── newsletter.rb
│   ├── webhook.php
│   └── notifications/
└── data/                   # Data storage
```

---

## ⚙️ Configuration

### Add Custom RSS Source

```python
from collect.rss_scraper import RSSScraper

scraper = RSSScraper()
scraper.add_source("My News", "https://example.com/feed.xml")
```

### Enable Dark/Light Theme

Toggle in the sidebar of the app.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit, JavaScript, CSS
- **Backend**: Python 3.12+, Java, Go
- **ML**: scikit-learn, NLTK
- **Search**: Rust (Fuse.js-style)
- **Storage**: JSON, SQLite ready

---

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md).

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file.

---

<div align="center">

**Built with ❤️ by [Nayak](https://github.com/Nayak-indie)**

</div>
