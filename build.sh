#!/bin/bash
# Tanya Build Script - Builds all non-Python components
# Run: ./build.sh

set -e

echo "========================================"
echo "  Tanya - Building Polyglot Components"
echo "========================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Build Rust
echo -e "\n${YELLOW}[1/4] Building Rust components...${NC}"
if command -v cargo &> /dev/null; then
    cd rust
    cargo build --release
    cd ..
    echo -e "${GREEN}✓ Rust binaries built${NC}"
else
    echo -e "${RED}✗ Cargo not found - skip Rust${NC}"
fi

# Build C++
echo -e "\n${YELLOW}[2/4] Building C++ components...${NC}"
if command -v g++ &> /dev/null; then
    cd cpp/src
    g++ -o ../bin/dedup dedup.cpp -std=c++17
    cd ../..
    echo -e "${GREEN}✓ C++ binaries built${NC}"
else
    echo -e "${RED}✗ g++ not found - skip C++${NC}"
fi

# Build Java
echo -e "\n${YELLOW}[3/4] Building Java components...${NC}"
if command -v javac &> /dev/null; then
    cd java/src
    javac APIServer.java
    cd ../..
    echo -e "${GREEN}✓ Java compiled${NC}"
else
    echo -e "${RED}✗ javac not found - skip Java${NC}"
fi

# Node.js
echo -e "\n${YELLOW}[4/4] Checking Node.js components...${NC}"
if command -v node &> /dev/null; then
    cd js/src
    node -c scraper.js && echo -e "${GREEN}✓ Node.js scripts valid${NC}" || echo -e "${RED}✗ Node.js syntax error${NC}"
    cd ../..
else
    echo -e "${RED}✗ Node.js not found - skip JS${NC}"
fi

echo -e "\n========================================"
echo -e "${GREEN}Build complete!${NC}"
echo "========================================"
echo ""
echo "To run Tanya:"
echo "  Streamlit: streamlit run app.py"
echo "  Rust CLI:  ./rust/target/release/rss_fetcher"
echo "  C++ CLI:   ./cpp/bin/dedup stats"
echo "  Java API:  cd java/src && java APIServer"
echo "  Node.js:   node js/src/scraper.js"
