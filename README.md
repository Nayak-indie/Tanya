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

Tanya (Trending And New Yielded Articles) is a **real polyglot news aggregator**—not a demo. Each language does actual work.

**Python is only ~20%** of the codebase. The rest is 22 other languages.

---

## 🏗️ Architecture

| Language | Component | What It Does |
|----------|-----------|--------------|
| **Python** | UI Layer | Streamlit web interface (~10%) |
| **Rust** | Core Engine | RSS fetching, full-text search, storage |
| **C++** | Processing | High-speed duplicate detection |
| **Go** | Worker | Background news fetching daemon |
| **Java** | API | REST API server |
| **Node.js** | Scraper | Alternative RSS scraper |
| **JavaScript** | Frontend | UI components |
| **C** | Parser | RSS parsing |
| **Kotlin** | Scraper | JVM-based scraper |
| **Julia** | Analytics | Scientific computing & stats |
| **Elixir** | Fetcher | Functional RSS fetcher |
| **Lua** | Scraper | Lightweight scraper |
| **Ada** | Validator | RSS validation |
| **Assembly** | Parser | Header parsing |
| **Perl** | Text | Text processing |
| **Fortran** | Stats | Statistical analysis |
| **R** | Analytics | Data analytics |
| **C#** | Notifications | Desktop notifications |
| **Ruby** | Newsletter | Newsletter delivery |
| **PHP** | Webhooks | HTTP callbacks |
| **Delphi** | Desktop | Desktop UI |
| **Scratch** | Prototype | Visual prototype |

---

## 🚀 Quick Start

### UI Only (Python)
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Full Polyglot
See [INSTALL.md](INSTALL.md) for all languages, then:
```bash
./build.sh
streamlit run app.py
```

---

## 🛠️ Usage by Language

| Language | Run Command |
|----------|-------------|
| Rust | `./rust/target/release/rss_fetcher` |
| C++ | `./cpp/bin/dedup stats` |
| Go | `go run go/cmd/worker.go --once` |
| Java | `cd java/src && java APIServer` |
| Node.js | `node js/src/scraper.js` |
| C | `gcc -o bin/parser c/rss_parser.c && ./bin/parser` |
| Kotlin | `kotlinc -include-runtime -d rss.jar kotlin/src/rss_scraper.kt` |
| Julia | `julia julia/src/analyzer.jl` |
| Elixir | `mix run elixir/lib/rss_fetcher.exs` |
| Lua | `lua lua/scraper.lua` |
| Ada | `gnatmake ada/src/ada_validator.adb` |
| Assembly | `nasm -f elf64 asm/src/asm_parser.asm && ld` |

---

## 📥 Installation

See [INSTALL.md](INSTALL.md) for complete setup on Ubuntu, macOS, Windows (WSL).

---

## 🤝 Contributing

Contributions in any language welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 📜 License

MIT License - see [LICENSE](LICENSE).

---

<div align="center">

**Built with ❤️ by [Nayak](https://github.com/Nayak-indie)**

*Python: 10% | 22 Other Languages: 90%*

</div>
