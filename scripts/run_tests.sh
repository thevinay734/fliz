#!/usr/bin/env bash
set -e

echo "🚀 Fliz Test Automation Runner"
echo "=============================="

# Load env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

ENV=${ENVIRONMENT:-dev}
HEADLESS=${HEADLESS:-true}

echo "Environment: $ENV"
echo "Headless:    $HEADLESS"
echo ""

# Clean old reports
rm -rf reports/allure-results/*
mkdir -p reports/allure-results logs

# Run API tests
echo "🧪 Running API tests..."
pytest -m api -v --alluredir=reports/allure-results

# Run UI tests
echo "🎭 Running UI tests..."
pytest -m ui -v --headed=false --alluredir=reports/allure-results

echo ""
echo "✅ Tests complete!"
echo "📊 Allure results: reports/allure-results/"
echo "📜 Logs:            logs/"
