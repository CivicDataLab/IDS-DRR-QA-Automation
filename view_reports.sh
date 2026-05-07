#!/bin/bash

# Report Viewer and Manager Script
# Helps view and manage timestamped test reports

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Function to print usage
usage() {
    echo ""
    echo "Usage: ./view_reports.sh [OPTION]"
    echo ""
    echo "Options:"
    echo "  -l, --latest           Open the latest HTML report (default)"
    echo "  -a, --all              List all HTML reports"
    echo "  -s, --self-healing     Show latest self-healing summary"
    echo "  -c, --clean [days]     Clean reports older than N days (default: 30)"
    echo "  -h, --help             Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./view_reports.sh                    # Open latest report"
    echo "  ./view_reports.sh --all              # List all reports"
    echo "  ./view_reports.sh --self-healing     # View healing summary"
    echo "  ./view_reports.sh --clean 7          # Delete reports older than 7 days"
    echo ""
}

# Function to open latest report
open_latest() {
    LATEST=$(ls -t reports/test_report_*.html 2>/dev/null | head -1)

    if [ -z "$LATEST" ]; then
        echo -e "${YELLOW}⚠️  No HTML reports found${NC}"
        echo "   Run tests first: pytest -n 4 -m smoke -v"
        exit 1
    fi

    echo -e "${GREEN}📊 Opening latest report:${NC} $LATEST"

    # Detect OS and open accordingly
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open "$LATEST"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open "$LATEST"
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        start "$LATEST"
    else
        echo "Please open manually: $LATEST"
    fi
}

# Function to list all reports
list_all() {
    echo -e "${BLUE}📋 HTML Test Reports:${NC}"
    echo ""

    if ! ls reports/test_report_*.html >/dev/null 2>&1; then
        echo -e "${YELLOW}   No reports found${NC}"
        return
    fi

    echo "  Date/Time           Size    File"
    echo "  ─────────────────────────────────────────────────────────"

    ls -lht reports/test_report_*.html | awk '{
        # Extract filename
        filename = $9
        # Extract date/time from filename (YYYYMMDD_HHMMSS)
        match(filename, /test_report_([0-9]{8})_([0-9]{6})\.html/, arr)
        if (arr[1] && arr[2]) {
            date = arr[1]
            time = arr[2]
            # Format: YYYY-MM-DD HH:MM:SS
            formatted = substr(date,1,4) "-" substr(date,5,2) "-" substr(date,7,2) " " substr(time,1,2) ":" substr(time,3,2) ":" substr(time,5,2)
            printf "  %s  %6s  %s\n", formatted, $5, filename
        }
    }'

    echo ""
    COUNT=$(ls reports/test_report_*.html 2>/dev/null | wc -l | tr -d ' ')
    echo -e "${GREEN}Total: $COUNT reports${NC}"
}

# Function to show self-healing summary
show_healing() {
    echo -e "${BLUE}🔧 Self-Healing Summary:${NC}"
    echo ""

    LATEST_SUMMARY=$(ls -t reports/self_healing/summary_*.txt 2>/dev/null | head -1)

    if [ -z "$LATEST_SUMMARY" ]; then
        echo -e "${YELLOW}   No self-healing summaries found${NC}"
        echo "   Run tests with self-healing enabled first"
        return
    fi

    cat "$LATEST_SUMMARY"
    echo ""
    echo -e "${GREEN}Report: $LATEST_SUMMARY${NC}"
}

# Function to clean old reports
clean_reports() {
    DAYS=${1:-30}

    echo -e "${YELLOW}🧹 Cleaning reports older than $DAYS days...${NC}"
    echo ""

    # Find and count old HTML reports
    OLD_HTML=$(find reports -name "test_report_*.html" -type f -mtime +$DAYS 2>/dev/null)
    HTML_COUNT=$(echo "$OLD_HTML" | grep -c "test_report_" || echo "0")

    # Find and count old JSON reports
    OLD_JSON=$(find reports -name "test_report_*.json" -type f -mtime +$DAYS 2>/dev/null)
    JSON_COUNT=$(echo "$OLD_JSON" | grep -c "test_report_" || echo "0")

    # Find and count old self-healing reports
    OLD_HEALING=$(find reports/self_healing -name "*.*" -type f -mtime +$DAYS 2>/dev/null)
    HEALING_COUNT=$(echo "$OLD_HEALING" | wc -l | tr -d ' ')

    if [ "$HTML_COUNT" -eq 0 ] && [ "$JSON_COUNT" -eq 0 ] && [ "$HEALING_COUNT" -eq 0 ]; then
        echo -e "${GREEN}✓ No old reports to clean${NC}"
        return
    fi

    echo "Found:"
    echo "  - $HTML_COUNT HTML reports"
    echo "  - $JSON_COUNT JSON reports"
    echo "  - $HEALING_COUNT self-healing reports"
    echo ""

    read -p "Delete these reports? (y/N): " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Delete old reports
        find reports -name "test_report_*.html" -type f -mtime +$DAYS -delete 2>/dev/null
        find reports -name "test_report_*.json" -type f -mtime +$DAYS -delete 2>/dev/null
        find reports/self_healing -name "*.*" -type f -mtime +$DAYS -delete 2>/dev/null

        echo -e "${GREEN}✓ Old reports deleted${NC}"
    else
        echo "Cancelled"
    fi
}

# Main script
case "${1:-}" in
    -l|--latest|"")
        open_latest
        ;;
    -a|--all)
        list_all
        ;;
    -s|--self-healing)
        show_healing
        ;;
    -c|--clean)
        clean_reports "${2:-30}"
        ;;
    -h|--help)
        usage
        ;;
    *)
        echo "Unknown option: $1"
        usage
        exit 1
        ;;
esac
