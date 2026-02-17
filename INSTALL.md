# Tanya Installation Guide

This guide helps you set up Tanya with all its polyglot components.

## Quick Start (Python Only - 10%)

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Full Installation (All 23 Languages)

### 1. Python (Required - UI Only)
```bash
pip install -r requirements.txt
pip install streamlit
```

### 2. Rust (RSS, Search, Storage)
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env
cd rust
cargo build --release
```

### 3. C++ (Duplicate Detection)
```bash
# Ubuntu
sudo apt-get install g++ make
cd cpp/src
g++ -o ../bin/dedup dedup.cpp -std=c++17
```

### 4. Go (Background Worker)
```bash
# Ubuntu
sudo apt-get install golang-go
cd go/cmd
go run worker.go --once
```

### 5. Java (REST API)
```bash
sudo apt-get install default-jdk
cd java/src
javac APIServer.java
java APIServer 8080
```

### 6. Node.js (Scraper)
```bash
sudo apt-get install nodejs npm
node js/src/scraper.js --all
```

### 7. C (RSS Parser)
```bash
sudo apt-get install libcurl4-openssl-dev libxml2-dev
gcc -o bin/rss_parser c/src/rss_parser.c -lcurl -lxml2
./bin/rss_parser
```

### 8. Kotlin (JVM Scraper)
```bash
# Ubuntu
sudo apt-get install kotlin
cd kotlin/src
kotlinc -include-runtime -d rss_scraper.jar rss_scraper.kt
kotlin -classpath rss_scraper.jar RssScraperKt
```

### 9. Julia (Analytics)
```bash
# Ubuntu
sudo apt-get install julia
julia -e 'import Pkg; Pkg.add("HTTP"); Pkg.add("JSON")'
julia julia/src/analyzer.jl
```

### 10. Elixir (Functional Fetcher)
```bash
# Ubuntu
sudo apt-get install elixir
mix local.hex --force
mix local.rebar --force
mix deps.get
mix run elixir/lib/rss_fetcher.exs
```

### 11. Lua (Lightweight Scraper)
```bash
# Ubuntu
sudo apt-get install lua5.3 liblua5.3-dev
# Or: luarocks install luasocket
lua lua/scraper.lua
```

### 12. Ada (RSS Validator)
```bash
# Ubuntu
sudo apt-get install gnat
cd ada/src
gnatmake ada_validator.adb
./ada_validator
```

### 13. Assembly (Header Parser)
```bash
# Ubuntu
sudo apt-get install nasm
cd asm/src
nasm -f elf64 -o asm_parser.o asm_parser.asm
ld -o bin/parser asm_parser.o
```

### 14. Perl (Text Processing)
```bash
# Comes pre-installed on most systems
perl core/text_processor.pl --help
```

### 15. Fortran (Statistics)
```bash
sudo apt-get install gfortran
gfortran -o bin/compute backend/ml/compute.f90
./bin/compute
```

### 16. R (Analytics)
```bash
sudo apt-get install r-base
Rscript backend/ml/analyze.R
```

### 17. C# (Notifications)
```bash
# Ubuntu
sudo apt-get install mono-mcs
mcs integrations/notifications/NotificationService.cs
mono NotificationService.exe
```

### 18. Ruby (Newsletter)
```bash
sudo apt-get install ruby
ruby integrations/newsletter.rb
```

### 19. PHP (Webhooks)
```bash
sudo apt-get install php
php integrations/webhook.php
```

### 20. Delphi (Desktop)
```bash
# Requires Delphi IDE (Windows) or Free Pascal
fpc integrations/desktop/tanya-desktop.pas
```

### 21. Scratch (Prototype)
- Open scratch/tanya_news.json in Scratch 3.0
- Or upload to https://scratch.mit.edu

---

## One-Liner Installs

### Ubuntu/Debian
```bash
sudo apt-get update && sudo apt-get install -y python3 python3-pip rustc cargo g++ make default-jdk golang-go nodejs npm lua5.3 liblua5.3-dev gnat nasm perl gfortran r-base ruby php mono-mcs kotlin julia elixir
```

### macOS
```bash
xcode-select --install
brew install rust node go lua kotlin julia elixir gcc gfortran R ruby php
```

---

## Verify Installation

```bash
./build.sh
```

---

## Troubleshooting

### Rust Build Fails
```bash
rustup update
cd rust && cargo clean && cargo build --release
```

### Port in Use
```bash
lsof -i :8080
kill -9 <PID>
```
