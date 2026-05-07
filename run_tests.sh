#!/bin/bash
# Run tests with HTML report

set -e

# Activate venv if exists
[ -d "venv" ] && source venv/bin/activate

# Create reports dir
mkdir -p reports

# Timestamp for report
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORT="reports/test_report_${TIMESTAMP}.html"

echo "Running tests..."
echo "Report: $REPORT"

# Run pytest
pytest tests/ --html=$REPORT --self-contained-html -v --tb=short

echo ""
echo "✅ Complete! Open report: open $REPORT"
