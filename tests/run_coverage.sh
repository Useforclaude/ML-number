#!/bin/bash
# 📍 วางไว้ที่: ML_Project_Refactored/run_coverage.sh

echo "🧪 Running Complete Test Suite with Coverage..."
echo "=============================================="

# Install test dependencies if needed
echo "📦 Installing test dependencies..."
pip install -r requirements-test.txt

# Clean previous coverage data
echo "🧹 Cleaning previous coverage data..."
rm -rf .coverage htmlcov/ coverage.xml

# Run all tests with coverage
echo "🏃 Running all tests..."
pytest tests/ \
    --cov=src \
    --cov-report=term-missing \
    --cov-report=html \
    --cov-report=xml \
    -v

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "✅ All tests passed!"
    
    # Generate coverage badge
    coverage-badge -o coverage.svg -f
    
    # Display coverage summary
    echo ""
    echo "📊 Coverage Summary:"
    echo "==================="
    coverage report
    
    # Open HTML report (if on macOS)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo ""
        echo "📂 Opening HTML coverage report..."
        open htmlcov/index.html
    else
        echo ""
        echo "📂 HTML coverage report generated at: htmlcov/index.html"
    fi
else
    echo "❌ Some tests failed. Please check the output above."
    exit 1
fi

# Performance test option
echo ""
echo "🚀 Run performance tests? (y/n)"
read -r response

if [[ "$response" == "y" ]]; then
    echo "⚡ Running performance tests..."
    pytest tests/test_performance.py -v -s
fi

echo ""
echo "✨ Test coverage analysis complete!"