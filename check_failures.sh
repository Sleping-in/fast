#!/bin/bash
BASE_URL="https://angelic-unity-production.up.railway.app"
YEAR=2025
EVENT="Bahrain"
DRIVER="VER"
SESSION_TYPE="R"

echo "Checking all endpoints for failures..."
echo "=================================================================================="
echo

FAILED=()
PASSED=()
NOT_FOUND=()

test_endpoint() {
    local endpoint=$1
    local description=$2
    local url="$BASE_URL$endpoint"
    
    status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 60 "$url")
    
    if [ "$status" = "200" ]; then
        PASSED+=("✅ $description (200)")
    elif [ "$status" = "404" ]; then
        NOT_FOUND+=("⚠️  $description (404 - Data not available)")
    elif [ "$status" = "000" ] || [ "$status" = "502" ] || [ "$status" = "503" ] || [ "$status" = "504" ]; then
        FAILED+=("❌ $description (Status: $status - Timeout/Error)")
    elif [ "$status" = "400" ]; then
        FAILED+=("❌ $description (400 - Bad Request)")
    elif [ "$status" = "500" ]; then
        FAILED+=("❌ $description (500 - Server Error)")
    else
        FAILED+=("❌ $description (Status: $status)")
    fi
}

# Test all endpoints
test_endpoint "/health" "Health check"
test_endpoint "/" "Root endpoint"
test_endpoint "/api/v1/sessions/$YEAR/$EVENT/$SESSION_TYPE" "Session info"
test_endpoint "/api/v1/results/$YEAR/$EVENT/qualifying/q1" "Q1 results"
test_endpoint "/api/v1/results/$YEAR/$EVENT/qualifying/q2" "Q2 results"
test_endpoint "/api/v1/results/$YEAR/$EVENT/qualifying/q3" "Q3 results"
test_endpoint "/api/v1/grid/$YEAR/$EVENT" "Grid positions"
test_endpoint "/api/v1/standings/$YEAR/drivers" "Driver standings"
test_endpoint "/api/v1/standings/$YEAR/constructors" "Constructor standings"
test_endpoint "/api/v1/teams/$YEAR/McLaren/results" "Team results"

echo "=================================================================================="
echo "❌ FAILED ENDPOINTS (Errors/Timeouts):"
echo "=================================================================================="
if [ ${#FAILED[@]} -eq 0 ]; then
    echo "None! All endpoints are working."
else
    for item in "${FAILED[@]}"; do
        echo "$item"
    done
fi

echo
echo "=================================================================================="
echo "⚠️  404 RESPONSES (Data not available - Expected):"
echo "=================================================================================="
if [ ${#NOT_FOUND[@]} -eq 0 ]; then
    echo "None."
else
    for item in "${NOT_FOUND[@]}"; do
        echo "$item"
    done
fi

echo
echo "=================================================================================="
echo "✅ WORKING ENDPOINTS: ${#PASSED[@]}"
echo "❌ FAILED ENDPOINTS: ${#FAILED[@]}"
echo "⚠️  404 (Data not available): ${#NOT_FOUND[@]}"
echo "=================================================================================="
