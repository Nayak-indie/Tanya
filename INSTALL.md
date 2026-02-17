# Tanya Installation Guide

This guide helps you set up Tanya with all its polyglot components.

## Quick Start (Python Only - 10%)

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## Full Installation (All Languages)

### 1. Python (Required)
```bash
# Install dependencies
pip install -r requirements.txt

# Install Streamlit
pip install streamlit
```

### 2. Rust (Search & RSS)
```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env

# Build Tanya components
cd rust
cargo build --release

# Run
./target/release/rss_fetcher --help
./target/release/search "tech"
```

### 3. C++ (Duplicate Detection)
```bash
# Ubuntu/Debian
sudo apt-get install g++ make

# macOS
xcode-select --install

# Build
cd cpp/src
g++ -o ../bin/dedup dedup.cpp -std=c++17

# Run
../bin/dedup stats
../bin/dedup dedup 0.8
```

### 4. Java (REST API)
```bash
# Ubuntu/Debian
sudo apt-get install default-jdk

# macOS
# Install from https://adoptopenjdk.net

# Compile & Run
cd java/src
javac APIServer.java
java APIServer 8080
```

### 5. Go (Background Worker)
```bash
# Ubuntu/Debian
sudo apt-get install golang-go

# macOS
brew install go

# Run
cd go/cmd
go run worker.go --once
go run worker.go --daemon --interval 15m
```

### 6. Node.js (Scraper)
```bash
# Ubuntu/Debian
sudo apt-get install nodejs npm

# macOS
brew install node

# Run
node js/src/scraper.js --help
node js/src/scraper.js --all
```

### 7. Perl (Text Processing)
```bash
# Ubuntu/Debian
sudo apt-get install perl

# macOS
# Comes pre-installed

# Run
perl core/text_processor.pl --help
```

### 8. Fortran (Statistics)
```bash
# Ubuntu/Debian
sudo apt-get install gfortran

# macOS
brew install gcc

# Compile
gfortran -o bin/compute backend/ml/compute.f90

# Run
./bin/compute
```

### 9. R (Analytics)
```bash
# Ubuntu/Debian
sudo apt-get install r-base

# macOS
brew install r

# Run
Rscript backend/ml/analyze.R
```

---

## Platform-Specific Installers

### Ubuntu/Debian One-Liner
```bash
sudo apt-get update && sudo apt-get install -y python3 python3-pip rustc cargo g++ default-jdk golang-go nodejs npm perl gfortran r-base
```

### macOS One-Liner
```bash
xcode-select --install
brew install rust node go perl gcc gfortran r
```

### Windows (WSL Recommended)
```bash
# Install WSL2, then use Ubuntu commands above
wsl --install
```

---

## Verify Installation

```bash
# Run build script
./build.sh

# Check all components
python3 -c "print('Python OK')"
rustc --version && cargo --version
g++ --version
java -version
node --version
go version
perl --version
```

---

## Troubleshooting

### Rust Build Fails
```bash
# Update Rust
rustup update

# Clean and rebuild
cd rust
cargo clean
cargo build --release
```

### Permission Denied
```bash
chmod +x build.sh
chmod +x rust/target/release/*
```

### Port Already in Use
```bash
# Find and kill process on port 8080
lsof -i :8080
kill -9 <PID>
```
