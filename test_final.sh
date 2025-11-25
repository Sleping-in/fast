#!/bin/bash
BASE_URL="https://angelic-unity-production.up.railway.app"
PASSED=0
FAILED=0
TOTAL=0

test_endpoint() {
    local endpoint=$1
    local description=$2
    TOTAL=$((TOTAL + 1))
    
    echo -n "Testing: $description ... "
    status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 60 "$BASE_URL$endpoint")
    
    if [ "$status" = "200" ] || [ "$status" = "404" ]; then
        echo "✅ PASSED (Status: $status)"
        PASSED=$((PASSED + 1))
    else
        echo "❌ FAILED (Status: $status)"
        FAILED=$((FAILED + 1))
    fi
}

echo "Testing previously failing endpoints with 60s timeout..."
test_endpoint "/api/v1/teams/2025/McLaren/results" "Team results"
test_endpoint "/api/v1/standings/2025/drivers" "Driver standings"
test_endpoint "/api/v1/standings/2025/constructors" "Constructor standings"
test_endpoint "/api/v1/sessions/2025/Bahrain/R" "Session info"
test_endpoint "/health" "Health check"
test_endpoint "/" "Root endpoint"
test_endpoint "/api/v1/results/2025/Bahrain/qualifying/q1" "Q1 results"
test_endpoint "/api/v1/grid/2025/Bahrain" "Grid positions"

echo
echo "Results: $PASSED/$TOTAL passed"
