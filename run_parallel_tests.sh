#!/bin/bash

# Parallel Test Execution Script
# This script provides easy commands to run tests with different parallel configurations

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to print usage
usage() {
    echo ""
    echo "Usage: ./run_parallel_tests.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help              Show this help message"
    echo "  -n, --workers <num>     Number of parallel workers (default: 4)"
    echo "  -t, --tests <path>      Test path (default: tests/)"
    echo "  -m, --marker <marker>   Run tests with specific marker (smoke, analytics, etc.)"
    echo "  -r, --reruns <num>      Number of times to rerun failed tests (default: 0)"
    echo "  --no-healing            Disable self-healing"
    echo "  --serial                Run tests serially (no parallel)"
    echo "  --auto                  Auto-detect number of workers"
    echo "  --skip-analytics        Skip test_analytics.py (runs all other tests)"
    echo ""
    echo "Examples:"
    echo "  ./run_parallel_tests.sh                          # Run with 4 workers"
    echo "  ./run_parallel_tests.sh -n 8                     # Run with 8 workers"
    echo "  ./run_parallel_tests.sh --auto                   # Auto-detect workers"
    echo "  ./run_parallel_tests.sh --skip-analytics -n 4    # Run all tests except test_analytics.py"
    echo "  ./run_parallel_tests.sh -m smoke -n 4            # Run smoke tests with 4 workers"
    echo "  ./run_parallel_tests.sh -n 4 -r 2                # Run with 4 workers, retry failures"
    echo "  ./run_parallel_tests.sh --serial                 # Run tests one by one"
    echo "  ./run_parallel_tests.sh -t tests/test_analytics.py -n 4  # Specific file"
    echo ""
}

# Default values
WORKERS=4
TEST_PATH="tests/"
MARKER=""
RERUNS=0
HEALING_FLAG=""
PARALLEL_FLAG="-n"
AUTO_WORKERS=""
SKIP_ANALYTICS=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -n|--workers)
            WORKERS="$2"
            shift 2
            ;;
        -t|--tests)
            TEST_PATH="$2"
            shift 2
            ;;
        -m|--marker)
            MARKER="-m $2"
            shift 2
            ;;
        -r|--reruns)
            RERUNS="$2"
            shift 2
            ;;
        --no-healing)
            HEALING_FLAG="--disable-healing"
            shift
            ;;
        --serial)
            PARALLEL_FLAG=""
            AUTO_WORKERS=""
            shift
            ;;
        --auto)
            AUTO_WORKERS="auto"
            shift
            ;;
        --skip-analytics)
            SKIP_ANALYTICS="--ignore=tests/test_analytics.py"
            shift
            ;;
        *)
            print_error "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Build the command
CMD="pytest"

# Add test path
CMD="$CMD $TEST_PATH"

# Add skip analytics flag if set
if [ -n "$SKIP_ANALYTICS" ]; then
    CMD="$CMD $SKIP_ANALYTICS"
    print_warning "Skipping test_analytics.py"
fi

# Add parallel workers
if [ -n "$PARALLEL_FLAG" ]; then
    if [ -n "$AUTO_WORKERS" ]; then
        CMD="$CMD -n auto"
        print_info "Running tests with auto-detected workers"
    else
        CMD="$CMD -n $WORKERS"
        print_info "Running tests with $WORKERS parallel workers"
    fi
else
    print_info "Running tests serially (no parallel execution)"
fi

# Add marker
if [ -n "$MARKER" ]; then
    CMD="$CMD $MARKER"
    print_info "Running tests with marker: $MARKER"
fi

# Add reruns
if [ "$RERUNS" -gt 0 ]; then
    CMD="$CMD --reruns $RERUNS --reruns-delay 1"
    print_info "Will retry failed tests $RERUNS times"
fi

# Add healing flag
if [ -n "$HEALING_FLAG" ]; then
    CMD="$CMD $HEALING_FLAG"
    print_warning "Self-healing is DISABLED"
else
    print_success "Self-healing is ENABLED"
fi

# Add verbose and other flags
CMD="$CMD -v"

# Print command
echo ""
print_info "Executing command:"
echo "  $CMD"
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    print_error "pytest is not installed. Please run: pip install -r requirements.txt"
    exit 1
fi

# Create reports directory
mkdir -p reports/self_healing

# Run the command
print_info "Starting test execution..."
echo "=============================================="
echo ""

if eval $CMD; then
    echo ""
    echo "=============================================="
    print_success "All tests completed successfully!"

    # Show reports
    if [ -d "reports/self_healing" ] && [ "$(ls -A reports/self_healing)" ]; then
        echo ""
        print_info "Self-healing reports generated:"
        ls -lh reports/self_healing/ | tail -n +2
    fi

    # Find the most recent HTML report
    LATEST_REPORT=$(ls -t reports/test_report_*.html 2>/dev/null | head -1)
    if [ -n "$LATEST_REPORT" ]; then
        echo ""
        print_info "HTML report: $LATEST_REPORT"
    fi

    exit 0
else
    echo ""
    echo "=============================================="
    print_error "Some tests failed. Check reports for details."

    # Find the most recent HTML report
    LATEST_REPORT=$(ls -t reports/test_report_*.html 2>/dev/null | head -1)
    if [ -n "$LATEST_REPORT" ]; then
        echo ""
        print_info "HTML report: $LATEST_REPORT"
    fi

    exit 1
fi
