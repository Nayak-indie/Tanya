# 📰 Tanya - Trending And New Yielded Articles

<div align="center">

![Python](https://img.shields.io/badge/python-3.12+-blue?style=for-the-badge&logo=python&logoColor=white)
![Rust](https://img.shields.io/badge/rust-DEA584?style=for-the-badge&logo=rust&logoColor=white)
![C++](https://img.shields.io/badge/c++-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white)
![Java](https://img.shields.io/badge/java-ED8B00?style=for-the-badge&logo=java&logoColor=white)
![Go](https://img.shields.io/badge/go-00ADD8?style=for-the-badge&logo=go&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

</div>

---

Tanya (Trending And New Yielded Articles) is a **real polyglot news aggregator**—not a demo or placeholder, but a fully functional app where each language does actual work.

**Python is only ~10%** of the codebase. The rest is Rust, C++, Java, Go, Node.js, and more.

---

## 🏗️ Architecture

| Language | Component | What It Does |
|----------|-----------|--------------|
| **Python** | UI Layer | Streamlit web interface (10%) |
| **Rust** | Core Engine | RSS fetching, full-text search, storage, deduplication |
| **C++** | Processing | High-speed duplicate detection |
| **Go** | Worker | Background news fetching daemon |
| **Java** | API | REST API server |
| **Node.js** | Scraper | Alternative RSS scraper |
| **Perl** | Text | Text processing utilities |
| **Fortran** | Stats | Statistical analysis |
| **R** | Analytics | Data analytics |

---

## 🚀 Quick Start

### Option 1: UI Only (Python)
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Option 2: Full Polyglot
See [INSTALL.md](INSTALL.md) for installing all languages, then:
```bash
# Build all components
./build.sh

# Run the app
streamlit run app.py
```

---

## 📁 Project Structure

```
Tanya/
├── app.py                    # Streamlit UI (Python - 10%)
├── rust/                     # RSS, Search, Storage (Rust)
│   └── src/
│       ├── rss_fetcher.rs
│       ├── search.rs
│       ├── storage.rs
│       └── dedup.rs
├── cpp/src/                 # Duplicate detection (C++)
│   └── dedup.cpp
├── go/cmd/                 # Background worker (Go)
│   └── worker.go
├── java/src/               # REST API (Java)
│   └── APIServer.java
├── js/src/                 # Alternative scraper (Node.js)
│   └── scraper.js
├── core/text_processor.pl   # Text processing (Perl)
├── backend/ml/compute.f90  # Statistics (Fortran)
├── backend/ml/analyze.R   # Analytics (R)
├── build.sh               # Build all components
└── INSTALL.md             # Full installation guide
```

---

## 🛠️ Usage

### Fetch News (Rust)
```bash
./rust/target/release/rss_fetcher
./rust/target/release/rss_fetcher https://example.com/feed.xml
```

### Search (Rust)
```bash
./rust/target/release/search "artificial intelligence"
./rust/target/release/search "tech" --limit 10
```

### Deduplicate (C++)
```bash
./cpp/bin/dedup stats
./cpp/bin/dedup dedup 0.8
./cpp/bin/dedup remove 0.8
```

### Run API Server (Java)
```bash
cd java/src
javac APIServer.java
java APIServer 8080
```

### Background Worker (Go)
```bash
cd go/cmd
go run worker.go --once           # Run once
go run worker.go --daemon         # Run continuously
```

### Scrape with Node.js
```bash
node js/src/scraper.js --all
node js/src/scraper.js --source BBC
```

---

## 📥 Installation

See [INSTALL.md](INSTALL.md) for complete installation instructions for each language on:
- Ubuntu/Debian
- macOS
- Windows (WSL)

---

## 🤝 Contributing

This is a polyglot experiment. Contributions in any language welcome!

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file.

---

<div align="center">

**Built with ❤️ by [Nayak](https://github.com/Nayak-indie)**

*Python: 10% | Everything else: 90%*

</div>
