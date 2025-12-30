#!/bin/bash

# Setup Verification Script
# Verifies that all dependencies and configurations are correct

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "Self-Healing & Parallel Execution Setup Verification"
echo "=========================================="
echo ""

# Check Python version
echo "1. Checking Python version..."
python_version=$(python3 --version 2>&1)
echo "   $python_version"
if [[ $python_version == *"3."* ]]; then
    echo -e "   ${GREEN}✓ Python 3.x found${NC}"
else
    echo -e "   ${RED}✗ Python 3.x required${NC}"
    exit 1
fi
echo ""

# Check if pytest is installed
echo "2. Checking pytest installation..."
if python3 -m pytest --version &> /dev/null; then
    pytest_version=$(python3 -m pytest --version 2>&1 | head -1)
    echo "   $pytest_version"
    echo -e "   ${GREEN}✓ pytest installed${NC}"
else
    echo -e "   ${RED}✗ pytest not installed${NC}"
    echo "   Run: pip install -r requirements.txt"
    exit 1
fi
echo ""

# Check pytest-xdist (parallel execution)
echo "3. Checking pytest-xdist (parallel execution)..."
if python3 -c "import xdist" 2>/dev/null; then
    echo -e "   ${GREEN}✓ pytest-xdist installed${NC}"
else
    echo -e "   ${RED}✗ pytest-xdist not installed${NC}"
    echo "   Run: pip install pytest-xdist"
    exit 1
fi
echo ""

# Check pytest-rerunfailures
echo "4. Checking pytest-rerunfailures..."
if python3 -c "import pytest_rerunfailures" 2>/dev/null; then
    echo -e "   ${GREEN}✓ pytest-rerunfailures installed${NC}"
else
    echo -e "   ${YELLOW}⚠ pytest-rerunfailures not installed (optional)${NC}"
    echo "   Run: pip install pytest-rerunfailures"
fi
echo ""

# Check pytest-html
echo "5. Checking pytest-html (reporting)..."
if python3 -c "import pytest_html" 2>/dev/null; then
    echo -e "   ${GREEN}✓ pytest-html installed${NC}"
else
    echo -e "   ${YELLOW}⚠ pytest-html not installed (optional)${NC}"
    echo "   Run: pip install pytest-html"
fi
echo ""

# Check directories
echo "6. Checking directory structure..."
if [ -d "tests" ]; then
    echo -e "   ${GREEN}✓ tests/ directory exists${NC}"
else
    echo -e "   ${RED}✗ tests/ directory not found${NC}"
    exit 1
fi

if [ -d "pages" ]; then
    echo -e "   ${GREEN}✓ pages/ directory exists${NC}"
else
    echo -e "   ${YELLOW}⚠ pages/ directory not found${NC}"
fi

if [ -d "utils" ]; then
    echo -e "   ${GREEN}✓ utils/ directory exists${NC}"
else
    echo -e "   ${RED}✗ utils/ directory not found${NC}"
    exit 1
fi
echo ""

# Check self-healing files
echo "7. Checking self-healing files..."
if [ -f "utils/self_healing.py" ]; then
    echo -e "   ${GREEN}✓ utils/self_healing.py exists${NC}"
else
    echo -e "   ${RED}✗ utils/self_healing.py not found${NC}"
    exit 1
fi

if [ -f "config/self_healing_config.py" ]; then
    echo -e "   ${GREEN}✓ config/self_healing_config.py exists${NC}"
else
    echo -e "   ${RED}✗ config/self_healing_config.py not found${NC}"
    exit 1
fi
echo ""

# Create necessary directories
echo "8. Creating necessary directories..."
mkdir -p reports/self_healing
mkdir -p config
echo -e "   ${GREEN}✓ Directories created${NC}"
echo ""

# Test collection
echo "9. Testing pytest collection (smoke tests)..."
if python3 -m pytest -m smoke --collect-only -q &> /dev/null; then
    test_count=$(python3 -m pytest -m smoke --collect-only -q 2>&1 | grep -c "test_" || echo "0")
    echo -e "   ${GREEN}✓ Found $test_count smoke tests${NC}"
else
    echo -e "   ${YELLOW}⚠ Could not collect tests (this is ok if no .env file)${NC}"
fi
echo ""

# Summary
echo "=========================================="
echo -e "${GREEN}Setup verification complete!${NC}"
echo "=========================================="
echo ""
echo "You can now run tests with:"
echo ""
echo "  # Standard execution"
echo "  pytest -m smoke -v"
echo ""
echo "  # Parallel execution (4 workers)"
echo "  pytest -n 4 -m smoke -v"
echo ""
echo "  # Auto-detect workers"
echo "  pytest -n auto -m smoke -v"
echo ""
echo "  # With auto-retry"
echo "  pytest -n 4 --reruns 2 -m smoke -v"
echo ""
echo "For more information, see:"
echo "  - QUICKSTART.md"
echo "  - SELF_HEALING_GUIDE.md"
echo "  - EXAMPLES.md"
echo ""
