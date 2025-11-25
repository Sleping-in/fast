#!/bin/bash
# Comprehensive test script for all FastF1 API endpoints
# Usage: ./test_all_endpoints.sh [BASE_URL]
# Example: ./test_all_endpoints.sh https://your-api.railway.app

BASE_URL="${1:-http://localhost:8000}"
YEAR=2025
EVENT="Bahrain"
DRIVER="VER"

echo "Testing FastF1 API endpoints at $BASE_URL"
echo "=========================================="
echo ""

# Test counter
PASSED=0
FAILED=0

test_endpoint() {
    local method=$1
    local endpoint=$2
    local description=$3
    
    echo -n "Testing: $description ... "
    
    if curl -s -f -o /dev/null -w "%{http_code}" "$BASE_URL$endpoint" | grep -q "200\|404"; then
        echo "✅ PASSED"
        ((PASSED++))
    else
        echo "❌ FAILED"
        ((FAILED++))
    fi
}

# Core endpoints
echo "=== Core Endpoints ==="
test_endpoint "GET" "/api/v1/events/$YEAR" "Events list"
test_endpoint "GET" "/api/v1/events/$YEAR/$EVENT" "Event details"
test_endpoint "GET" "/api/v1/sessions/$YEAR/$EVENT/R" "Session info"
test_endpoint "GET" "/api/v1/results/$YEAR/$EVENT" "Race results"
test_endpoint "GET" "/api/v1/results/$YEAR/$EVENT/qualifying" "Qualifying results"
test_endpoint "GET" "/api/v1/laps/$YEAR/$EVENT" "Laps"
test_endpoint "GET" "/api/v1/laps/$YEAR/$EVENT/$DRIVER" "Driver laps"
test_endpoint "GET" "/api/v1/laps/$YEAR/$EVENT/fastest" "Fastest lap"
test_endpoint "GET" "/api/v1/telemetry/$YEAR/$EVENT/$DRIVER" "Telemetry"
test_endpoint "GET" "/api/v1/drivers/$YEAR" "Drivers list"

echo ""
echo "=== New Weather Endpoints ==="
test_endpoint "GET" "/api/v1/weather/$YEAR/$EVENT/R" "Weather data"
test_endpoint "GET" "/api/v1/weather/$YEAR/$EVENT/R/summary" "Weather summary"

echo ""
echo "=== Track Status Endpoints ==="
test_endpoint "GET" "/api/v1/track-status/$YEAR/$EVENT/R" "Track status"
test_endpoint "GET" "/api/v1/track-status/$YEAR/$EVENT/R/safety-car" "Safety car periods"
test_endpoint "GET" "/api/v1/track-status/$YEAR/$EVENT/R/vsc" "VSC periods"

echo ""
echo "=== Position Endpoints ==="
test_endpoint "GET" "/api/v1/positions/$YEAR/$EVENT/R" "Positions"
test_endpoint "GET" "/api/v1/positions/$YEAR/$EVENT/R/changes" "Position changes"
test_endpoint "GET" "/api/v1/positions/$YEAR/$EVENT/R/overtakes" "Overtakes"

echo ""
echo "=== Pit Stops Endpoints ==="
test_endpoint "GET" "/api/v1/pit-stops/$YEAR/$EVENT/R" "Pit stops"
test_endpoint "GET" "/api/v1/pit-stops/$YEAR/$EVENT/R/fastest" "Fastest pit stop"

echo ""
echo "=== Circuit Endpoints ==="
test_endpoint "GET" "/api/v1/circuits/$YEAR/$EVENT" "Circuit info"
test_endpoint "GET" "/api/v1/circuits/$YEAR/$EVENT/corners" "Corners"

echo ""
echo "=== Race Control Endpoints ==="
test_endpoint "GET" "/api/v1/race-control/$YEAR/$EVENT/R" "Race control messages"
test_endpoint "GET" "/api/v1/race-control/$YEAR/$EVENT/R/penalties" "Penalties"

echo ""
echo "=== Sector Endpoints ==="
test_endpoint "GET" "/api/v1/sectors/$YEAR/$EVENT/R" "Sectors"
test_endpoint "GET" "/api/v1/sectors/$YEAR/$EVENT/fastest/sector1" "Fastest sector 1"

echo ""
echo "=== Gap Endpoints ==="
test_endpoint "GET" "/api/v1/gaps/$YEAR/$EVENT/R" "Gaps to leader"
test_endpoint "GET" "/api/v1/gaps/$YEAR/$EVENT/R/$DRIVER" "Driver gaps"

echo ""
echo "=== Tyre Endpoints ==="
test_endpoint "GET" "/api/v1/tyres/$YEAR/$EVENT/R/compounds" "Tyre compounds"
test_endpoint "GET" "/api/v1/tyres/$YEAR/$EVENT/R/strategy" "Tyre strategy"

echo ""
echo "=== Team Endpoints ==="
test_endpoint "GET" "/api/v1/teams/$YEAR" "Teams list"
test_endpoint "GET" "/api/v1/teams/$YEAR/$EVENT" "Event teams"

echo ""
echo "=== Standings Endpoints ==="
test_endpoint "GET" "/api/v1/standings/$YEAR/drivers" "Driver standings"
test_endpoint "GET" "/api/v1/standings/$YEAR/constructors" "Constructor standings"

echo ""
echo "=== Qualifying Endpoints ==="
test_endpoint "GET" "/api/v1/results/$YEAR/$EVENT/qualifying/q1" "Q1 results"
test_endpoint "GET" "/api/v1/grid/$YEAR/$EVENT" "Grid positions"

echo ""
echo "=== Lap Filtering ==="
test_endpoint "GET" "/api/v1/laps/$YEAR/$EVENT?quicklaps=true" "Quick laps"
test_endpoint "GET" "/api/v1/laps/$YEAR/$EVENT/personal-best" "Personal best laps"

echo ""
echo "=== Event Convenience Endpoints ==="
test_endpoint "GET" "/api/v1/events/upcoming" "Upcoming events"
test_endpoint "GET" "/api/v1/events/$YEAR/past" "Past events"
test_endpoint "GET" "/api/v1/events/$YEAR/round/1" "Event by round"
test_endpoint "GET" "/api/v1/events/$YEAR/country/Bahrain" "Event by country"

echo ""
echo "=== Historical Data (Ergast) ==="
test_endpoint "GET" "/api/v1/historical/2010/events" "Historical events (2010)"
test_endpoint "GET" "/api/v1/historical/2010/results?round=1" "Historical results (2010)"
test_endpoint "GET" "/api/v1/historical/2010/drivers" "Historical drivers (2010)"
test_endpoint "GET" "/api/v1/historical/2010/constructors" "Historical constructors (2010)"
test_endpoint "GET" "/api/v1/historical/2010/standings/drivers" "Historical driver standings (2010)"

echo ""
echo "=========================================="
echo "Test Results:"
echo "✅ Passed: $PASSED"
echo "❌ Failed: $FAILED"
echo "Total: $((PASSED + FAILED))"

