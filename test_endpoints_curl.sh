#!/bin/bash
BASE_URL="${1:-https://angelic-unity-production.up.railway.app}"
YEAR=2025
EVENT="Bahrain"
DRIVER="VER"
SESSION_TYPE="R"

PASSED=0
FAILED=0
TOTAL=0

test_endpoint() {
    local endpoint=$1
    local description=$2
    TOTAL=$((TOTAL + 1))
    
    echo -n "Testing: $description ... "
    status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 30 "$BASE_URL$endpoint")
    
    if [ "$status" = "200" ] || [ "$status" = "404" ]; then
        echo "✅ PASSED (Status: $status)"
        PASSED=$((PASSED + 1))
    else
        echo "❌ FAILED (Status: $status)"
        FAILED=$((FAILED + 1))
    fi
}

echo "=================================================================================="
echo "Testing FastF1 API at: $BASE_URL"
echo "Year: $YEAR, Event: $EVENT, Driver: $DRIVER, Session: $SESSION_TYPE"
echo "=================================================================================="
echo

echo "📋 CORE ENDPOINTS"
echo "----------------------------------------------------------------------------------"
test_endpoint "/api/v1/events/$YEAR" "Events list"
test_endpoint "/api/v1/events/$YEAR/$EVENT" "Event details"
test_endpoint "/api/v1/sessions/$YEAR/$EVENT/$SESSION_TYPE" "Session info"
test_endpoint "/api/v1/results/$YEAR/$EVENT" "Race results"
test_endpoint "/api/v1/results/$YEAR/$EVENT/qualifying" "Qualifying results"
test_endpoint "/api/v1/results/$YEAR/$EVENT/sprint" "Sprint results"
test_endpoint "/api/v1/results/$YEAR/$EVENT/sprint-qualifying" "Sprint qualifying results"
test_endpoint "/api/v1/drivers/$YEAR" "Drivers list"
test_endpoint "/api/v1/drivers/$YEAR/$EVENT" "Event drivers"
echo

echo "🏁 LAPS ENDPOINTS"
echo "----------------------------------------------------------------------------------"
test_endpoint "/api/v1/laps/$YEAR/$EVENT?session_type=$SESSION_TYPE" "All laps"
test_endpoint "/api/v1/laps/$YEAR/$EVENT/$DRIVER?session_type=$SESSION_TYPE" "Driver laps"
test_endpoint "/api/v1/laps/$YEAR/$EVENT/fastest?session_type=$SESSION_TYPE" "Fastest lap"
test_endpoint "/api/v1/laps/$YEAR/$EVENT/personal-best?session_type=$SESSION_TYPE" "Personal best laps"
test_endpoint "/api/v1/laps/$YEAR/$EVENT?session_type=$SESSION_TYPE&quicklaps=true" "Quick laps filter"
test_endpoint "/api/v1/laps/$YEAR/$EVENT?session_type=$SESSION_TYPE&compound=SOFT" "Laps by compound"
echo

echo "📊 TELEMETRY ENDPOINTS"
echo "----------------------------------------------------------------------------------"
test_endpoint "/api/v1/telemetry/$YEAR/$EVENT/$DRIVER?session_type=$SESSION_TYPE" "Driver telemetry"
test_endpoint "/api/v1/telemetry/$YEAR/$EVENT/$DRIVER?session_type=$SESSION_TYPE&lap=1" "Telemetry for lap 1"
test_endpoint "/api/v1/car-data/$YEAR/$EVENT/$DRIVER?session_type=$SESSION_TYPE" "Car data"
test_endpoint "/api/v1/telemetry/$YEAR/$EVENT/$DRIVER/drs?session_type=$SESSION_TYPE" "DRS data"
test_endpoint "/api/v1/telemetry/$YEAR/$EVENT/$DRIVER/speed?session_type=$SESSION_TYPE" "Speed data"
echo

echo "🌤️  WEATHER ENDPOINTS"
echo "----------------------------------------------------------------------------------"
test_endpoint "/api/v1/weather/$YEAR/$EVENT/$SESSION_TYPE" "Weather data"
test_endpoint "/api/v1/weather/$YEAR/$EVENT/$SESSION_TYPE/summary" "Weather summary"
echo

echo "🚩 TRACK STATUS ENDPOINTS"
echo "----------------------------------------------------------------------------------"
test_endpoint "/api/v1/track-status/$YEAR/$EVENT/$SESSION_TYPE" "Track status"
test_endpoint "/api/v1/track-status/$YEAR/$EVENT/$SESSION_TYPE/safety-car" "Safety car periods"
test_endpoint "/api/v1/track-status/$YEAR/$EVENT/$SESSION_TYPE/vsc" "VSC periods"
test_endpoint "/api/v1/track-status/$YEAR/$EVENT/$SESSION_TYPE/red-flags" "Red flag periods"
test_endpoint "/api/v1/track-status/$YEAR/$EVENT/$SESSION_TYPE/yellow-flags" "Yellow flag periods"
echo

echo "📍 POSITION ENDPOINTS"
echo "----------------------------------------------------------------------------------"
test_endpoint "/api/v1/positions/$YEAR/$EVENT/$SESSION_TYPE" "Position data"
test_endpoint "/api/v1/positions/$YEAR/$EVENT/$SESSION_TYPE/$DRIVER" "Driver positions"
test_endpoint "/api/v1/positions/$YEAR/$EVENT/$SESSION_TYPE/changes" "Position changes"
test_endpoint "/api/v1/positions/$YEAR/$EVENT/$SESSION_TYPE/overtakes" "Overtakes"
echo

echo "🛑 PIT STOPS ENDPOINTS"
echo "----------------------------------------------------------------------------------"
test_endpoint "/api/v1/pit-stops/$YEAR/$EVENT/$SESSION_TYPE" "Pit stops"
test_endpoint "/api/v1/pit-stops/$YEAR/$EVENT/$SESSION_TYPE?include_duration=true" "Pit stops with duration"
test_endpoint "/api/v1/pit-stops/$YEAR/$EVENT/$SESSION_TYPE/$DRIVER" "Driver pit stops"
test_endpoint "/api/v1/pit-stops/$YEAR/$EVENT/$SESSION_TYPE/fastest" "Fastest pit stop"
test_endpoint "/api/v1/pit-stops/$YEAR/$EVENT/$SESSION_TYPE/strategy" "Pit stop strategy"
echo

echo "🏎️  CIRCUIT ENDPOINTS"
echo "----------------------------------------------------------------------------------"
test_endpoint "/api/v1/circuits/$YEAR/$EVENT" "Circuit info"
test_endpoint "/api/v1/circuits/$YEAR/$EVENT/drs-zones" "DRS zones"
test_endpoint "/api/v1/circuits/$YEAR/$EVENT/markers" "Track markers"
test_endpoint "/api/v1/circuits/$YEAR/$EVENT/corners" "Corners"
test_endpoint "/api/v1/circuits/$YEAR/$EVENT/marshal-sectors" "Marshal sectors"
echo

echo "📢 RACE CONTROL ENDPOINTS"
echo "----------------------------------------------------------------------------------"
test_endpoint "/api/v1/race-control/$YEAR/$EVENT/$SESSION_TYPE" "Race control messages"
test_endpoint "/api/v1/race-control/$YEAR/$EVENT/$SESSION_TYPE/penalties" "Penalties"
test_endpoint "/api/v1/race-control/$YEAR/$EVENT/$SESSION_TYPE/investigations" "Investigations"
echo

echo "⏱️  SECTOR ENDPOINTS"
echo "----------------------------------------------------------------------------------"
test_endpoint "/api/v1/sectors/$YEAR/$EVENT/$SESSION_TYPE" "All sectors"
test_endpoint "/api/v1/sectors/$YEAR/$EVENT/$SESSION_TYPE/$DRIVER" "Driver sectors"
test_endpoint "/api/v1/sectors/$YEAR/$EVENT/fastest/sector1?session_type=$SESSION_TYPE" "Fastest sector 1"
test_endpoint "/api/v1/sectors/$YEAR/$EVENT/fastest/sector2?session_type=$SESSION_TYPE" "Fastest sector 2"
test_endpoint "/api/v1/sectors/$YEAR/$EVENT/fastest/sector3?session_type=$SESSION_TYPE" "Fastest sector 3"
echo

echo "📏 GAP ENDPOINTS"
echo "----------------------------------------------------------------------------------"
test_endpoint "/api/v1/gaps/$YEAR/$EVENT/$SESSION_TYPE" "Gaps to leader"
test_endpoint "/api/v1/gaps/$YEAR/$EVENT/$SESSION_TYPE?lap=10" "Gaps at lap 10"
test_endpoint "/api/v1/gaps/$YEAR/$EVENT/$SESSION_TYPE/$DRIVER" "Driver gaps"
test_endpoint "/api/v1/gaps/$YEAR/$EVENT/$SESSION_TYPE/$DRIVER/ahead" "Gap to driver ahead"
test_endpoint "/api/v1/gaps/$YEAR/$EVENT/$SESSION_TYPE/$DRIVER/behind" "Gap to driver behind"
echo

echo "🛞 TYRE ENDPOINTS"
echo "----------------------------------------------------------------------------------"
test_endpoint "/api/v1/tyres/$YEAR/$EVENT/$SESSION_TYPE/compounds" "Tyre compounds"
test_endpoint "/api/v1/tyres/$YEAR/$EVENT/$SESSION_TYPE/strategy" "Tyre strategy"
test_endpoint "/api/v1/tyres/$YEAR/$EVENT/$SESSION_TYPE/$DRIVER/stints" "Driver stints"
test_endpoint "/api/v1/tyres/$YEAR/$EVENT/$SESSION_TYPE/life-analysis" "Tyre life analysis"
echo

echo "🏆 TEAM ENDPOINTS"
echo "----------------------------------------------------------------------------------"
test_endpoint "/api/v1/teams/$YEAR" "Teams list"
test_endpoint "/api/v1/teams/$YEAR/$EVENT" "Event teams"
test_endpoint "/api/v1/teams/$YEAR/McLaren/results" "Team results"
echo

echo "📈 STANDINGS ENDPOINTS"
echo "----------------------------------------------------------------------------------"
test_endpoint "/api/v1/standings/$YEAR/drivers" "Driver standings"
test_endpoint "/api/v1/standings/$YEAR/constructors" "Constructor standings"
test_endpoint "/api/v1/standings/$YEAR/drivers/after/$EVENT" "Driver standings after event"
test_endpoint "/api/v1/standings/$YEAR/constructors/after/$EVENT" "Constructor standings after event"
echo

echo "🏁 QUALIFYING ENDPOINTS"
echo "----------------------------------------------------------------------------------"
test_endpoint "/api/v1/results/$YEAR/$EVENT/qualifying/q1" "Q1 results"
test_endpoint "/api/v1/results/$YEAR/$EVENT/qualifying/q2" "Q2 results"
test_endpoint "/api/v1/results/$YEAR/$EVENT/qualifying/q3" "Q3 results"
test_endpoint "/api/v1/grid/$YEAR/$EVENT" "Grid positions"
echo

echo "💚 HEALTH CHECK"
echo "----------------------------------------------------------------------------------"
test_endpoint "/health" "Health check"
test_endpoint "/" "Root endpoint"
echo

echo "=================================================================================="
echo "TEST SUMMARY"
echo "=================================================================================="
echo "Total Endpoints Tested: $TOTAL"
echo "✅ Passed: $PASSED"
echo "❌ Failed: $FAILED"
echo "Success Rate: $(( PASSED * 100 / TOTAL ))%"
echo "=================================================================================="
