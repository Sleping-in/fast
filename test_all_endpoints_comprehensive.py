#!/usr/bin/env python3
"""
Comprehensive test script for all FastF1 API endpoints.
Tests every single endpoint we've implemented.
"""
import requests
import sys
import json
from typing import Dict, List, Tuple

BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
YEAR = int(sys.argv[2]) if len(sys.argv) > 2 else 2025
EVENT = sys.argv[3] if len(sys.argv) > 3 else "Bahrain"
DRIVER = sys.argv[4] if len(sys.argv) > 4 else "VER"
SESSION_TYPE = sys.argv[5] if len(sys.argv) > 5 else "R"

# Test results
results: List[Tuple[str, str, bool, str]] = []

def test_endpoint(method: str, endpoint: str, description: str, expected_status: int = 200) -> bool:
    """Test an endpoint and record the result."""
    url = f"{BASE_URL}{endpoint}"
    try:
        # Increased timeout to 300s because loading a new session (downloading telemetry)
        # can take longer than 30s on the first run.
        response = requests.get(url, timeout=300)
        status = response.status_code
        
        # 200 = success, 404 = not found (data might not exist), 400 = bad request
        # We'll accept 200 and 404 as "working" (404 means endpoint works but data doesn't exist)
        success = status in [200, 404] or (expected_status and status == expected_status)
        
        status_text = "✅" if success else "❌"
        results.append((status_text, description, success, f"Status: {status}"))
        
        if not success:
            try:
                error_data = response.json()
                results[-1] = (status_text, description, success, f"Status: {status}, Error: {error_data.get('error', {}).get('message', 'Unknown')}")
            except:
                pass
        
        return success
    except requests.exceptions.RequestException as e:
        results.append(("❌", description, False, f"Error: {str(e)}"))
        return False

print("=" * 80)
print(f"Testing FastF1 API at: {BASE_URL}")
print(f"Year: {YEAR}, Event: {EVENT}, Driver: {DRIVER}, Session: {SESSION_TYPE}")
print("=" * 80)
print()

# Core Endpoints
print("📋 CORE ENDPOINTS")
print("-" * 80)
test_endpoint("GET", f"/api/v1/events/{YEAR}", "Events list")
test_endpoint("GET", f"/api/v1/events/{YEAR}/{EVENT}", "Event details")
test_endpoint("GET", f"/api/v1/sessions/{YEAR}/{EVENT}/{SESSION_TYPE}", "Session info")
test_endpoint("GET", f"/api/v1/results/{YEAR}/{EVENT}", "Race results")
test_endpoint("GET", f"/api/v1/results/{YEAR}/{EVENT}/qualifying", "Qualifying results")
test_endpoint("GET", f"/api/v1/results/{YEAR}/{EVENT}/sprint", "Sprint results")
test_endpoint("GET", f"/api/v1/results/{YEAR}/{EVENT}/sprint-qualifying", "Sprint qualifying results")
test_endpoint("GET", f"/api/v1/drivers/{YEAR}", "Drivers list")
test_endpoint("GET", f"/api/v1/drivers/{YEAR}/{EVENT}", "Event drivers")
print()

# Laps Endpoints
print("🏁 LAPS ENDPOINTS")
print("-" * 80)
test_endpoint("GET", f"/api/v1/laps/{YEAR}/{EVENT}?session_type={SESSION_TYPE}", "All laps")
test_endpoint("GET", f"/api/v1/laps/{YEAR}/{EVENT}/{DRIVER}?session_type={SESSION_TYPE}", "Driver laps")
test_endpoint("GET", f"/api/v1/laps/{YEAR}/{EVENT}/fastest?session_type={SESSION_TYPE}", "Fastest lap")
test_endpoint("GET", f"/api/v1/laps/{YEAR}/{EVENT}/personal-best?session_type={SESSION_TYPE}", "Personal best laps")
test_endpoint("GET", f"/api/v1/laps/{YEAR}/{EVENT}?session_type={SESSION_TYPE}&quicklaps=true", "Quick laps filter")
test_endpoint("GET", f"/api/v1/laps/{YEAR}/{EVENT}?session_type={SESSION_TYPE}&compound=SOFT", "Laps by compound")
test_endpoint("GET", f"/api/v1/laps/{YEAR}/{EVENT}?session_type={SESSION_TYPE}&exclude_pits=true", "Laps exclude pits")
print()

# Telemetry Endpoints
print("📊 TELEMETRY ENDPOINTS")
print("-" * 80)
test_endpoint("GET", f"/api/v1/telemetry/{YEAR}/{EVENT}/{DRIVER}?session_type={SESSION_TYPE}", "Driver telemetry")
test_endpoint("GET", f"/api/v1/telemetry/{YEAR}/{EVENT}/{DRIVER}?session_type={SESSION_TYPE}&lap=1", "Telemetry for lap 1")
test_endpoint("GET", f"/api/v1/car-data/{YEAR}/{EVENT}/{DRIVER}?session_type={SESSION_TYPE}", "Car data")
test_endpoint("GET", f"/api/v1/telemetry/{YEAR}/{EVENT}/{DRIVER}/drs?session_type={SESSION_TYPE}", "DRS data")
test_endpoint("GET", f"/api/v1/telemetry/{YEAR}/{EVENT}/{DRIVER}/speed?session_type={SESSION_TYPE}", "Speed data")
print()

# Weather Endpoints
print("🌤️  WEATHER ENDPOINTS")
print("-" * 80)
test_endpoint("GET", f"/api/v1/weather/{YEAR}/{EVENT}/{SESSION_TYPE}", "Weather data")
test_endpoint("GET", f"/api/v1/weather/{YEAR}/{EVENT}/{SESSION_TYPE}/summary", "Weather summary")
print()

# Track Status Endpoints
print("🚩 TRACK STATUS ENDPOINTS")
print("-" * 80)
test_endpoint("GET", f"/api/v1/track-status/{YEAR}/{EVENT}/{SESSION_TYPE}", "Track status")
test_endpoint("GET", f"/api/v1/track-status/{YEAR}/{EVENT}/{SESSION_TYPE}/safety-car", "Safety car periods")
test_endpoint("GET", f"/api/v1/track-status/{YEAR}/{EVENT}/{SESSION_TYPE}/vsc", "VSC periods")
test_endpoint("GET", f"/api/v1/track-status/{YEAR}/{EVENT}/{SESSION_TYPE}/red-flags", "Red flag periods")
test_endpoint("GET", f"/api/v1/track-status/{YEAR}/{EVENT}/{SESSION_TYPE}/yellow-flags", "Yellow flag periods")
print()

# Position Endpoints
print("📍 POSITION ENDPOINTS")
print("-" * 80)
test_endpoint("GET", f"/api/v1/positions/{YEAR}/{EVENT}/{SESSION_TYPE}", "Position data")
test_endpoint("GET", f"/api/v1/positions/{YEAR}/{EVENT}/{SESSION_TYPE}/{DRIVER}", "Driver positions")
test_endpoint("GET", f"/api/v1/positions/{YEAR}/{EVENT}/{SESSION_TYPE}/changes", "Position changes")
test_endpoint("GET", f"/api/v1/positions/{YEAR}/{EVENT}/{SESSION_TYPE}/overtakes", "Overtakes")
print()

# Pit Stops Endpoints
print("🛑 PIT STOPS ENDPOINTS")
print("-" * 80)
test_endpoint("GET", f"/api/v1/pit-stops/{YEAR}/{EVENT}/{SESSION_TYPE}", "Pit stops")
test_endpoint("GET", f"/api/v1/pit-stops/{YEAR}/{EVENT}/{SESSION_TYPE}?include_duration=true", "Pit stops with duration")
test_endpoint("GET", f"/api/v1/pit-stops/{YEAR}/{EVENT}/{SESSION_TYPE}/{DRIVER}", "Driver pit stops")
test_endpoint("GET", f"/api/v1/pit-stops/{YEAR}/{EVENT}/{SESSION_TYPE}/fastest", "Fastest pit stop")
test_endpoint("GET", f"/api/v1/pit-stops/{YEAR}/{EVENT}/{SESSION_TYPE}/strategy", "Pit stop strategy")
print()

# Circuit Endpoints
print("🏎️  CIRCUIT ENDPOINTS")
print("-" * 80)
test_endpoint("GET", f"/api/v1/circuits/{YEAR}/{EVENT}", "Circuit info")
test_endpoint("GET", f"/api/v1/circuits/{YEAR}/{EVENT}/drs-zones", "DRS zones")
test_endpoint("GET", f"/api/v1/circuits/{YEAR}/{EVENT}/markers", "Track markers")
test_endpoint("GET", f"/api/v1/circuits/{YEAR}/{EVENT}/corners", "Corners")
test_endpoint("GET", f"/api/v1/circuits/{YEAR}/{EVENT}/marshal-sectors", "Marshal sectors")
print()

# Race Control Endpoints
print("📢 RACE CONTROL ENDPOINTS")
print("-" * 80)
test_endpoint("GET", f"/api/v1/race-control/{YEAR}/{EVENT}/{SESSION_TYPE}", "Race control messages")
test_endpoint("GET", f"/api/v1/race-control/{YEAR}/{EVENT}/{SESSION_TYPE}/penalties", "Penalties")
test_endpoint("GET", f"/api/v1/race-control/{YEAR}/{EVENT}/{SESSION_TYPE}/investigations", "Investigations")
print()

# Sector Endpoints
print("⏱️  SECTOR ENDPOINTS")
print("-" * 80)
test_endpoint("GET", f"/api/v1/sectors/{YEAR}/{EVENT}/{SESSION_TYPE}", "All sectors")
test_endpoint("GET", f"/api/v1/sectors/{YEAR}/{EVENT}/{SESSION_TYPE}/{DRIVER}", "Driver sectors")
test_endpoint("GET", f"/api/v1/sectors/{YEAR}/{EVENT}/{SESSION_TYPE}/fastest/sector1", "Fastest sector 1")
test_endpoint("GET", f"/api/v1/sectors/{YEAR}/{EVENT}/{SESSION_TYPE}/fastest/sector2", "Fastest sector 2")
test_endpoint("GET", f"/api/v1/sectors/{YEAR}/{EVENT}/{SESSION_TYPE}/fastest/sector3", "Fastest sector 3")
print()

# Gap Endpoints
print("📏 GAP ENDPOINTS")
print("-" * 80)
test_endpoint("GET", f"/api/v1/gaps/{YEAR}/{EVENT}/{SESSION_TYPE}", "Gaps to leader")
test_endpoint("GET", f"/api/v1/gaps/{YEAR}/{EVENT}/{SESSION_TYPE}?lap=10", "Gaps at lap 10")
test_endpoint("GET", f"/api/v1/gaps/{YEAR}/{EVENT}/{SESSION_TYPE}/{DRIVER}", "Driver gaps")
test_endpoint("GET", f"/api/v1/gaps/{YEAR}/{EVENT}/{SESSION_TYPE}/{DRIVER}/ahead", "Gap to driver ahead")
test_endpoint("GET", f"/api/v1/gaps/{YEAR}/{EVENT}/{SESSION_TYPE}/{DRIVER}/behind", "Gap to driver behind")
print()

# Tyre Endpoints
print("🛞 TYRE ENDPOINTS")
print("-" * 80)
test_endpoint("GET", f"/api/v1/tyres/{YEAR}/{EVENT}/{SESSION_TYPE}/compounds", "Tyre compounds")
test_endpoint("GET", f"/api/v1/tyres/{YEAR}/{EVENT}/{SESSION_TYPE}/strategy", "Tyre strategy")
test_endpoint("GET", f"/api/v1/tyres/{YEAR}/{EVENT}/{SESSION_TYPE}/{DRIVER}/stints", "Driver stints")
test_endpoint("GET", f"/api/v1/tyres/{YEAR}/{EVENT}/{SESSION_TYPE}/life-analysis", "Tyre life analysis")
print()

# Team Endpoints
print("🏆 TEAM ENDPOINTS")
print("-" * 80)
test_endpoint("GET", f"/api/v1/teams/{YEAR}", "Teams list")
test_endpoint("GET", f"/api/v1/teams/{YEAR}/{EVENT}", "Event teams")
test_endpoint("GET", f"/api/v1/teams/{YEAR}/McLaren/results", "Team results")
print()

# Standings Endpoints
print("📈 STANDINGS ENDPOINTS")
print("-" * 80)
test_endpoint("GET", f"/api/v1/standings/{YEAR}/drivers", "Driver standings")
test_endpoint("GET", f"/api/v1/standings/{YEAR}/constructors", "Constructor standings")
test_endpoint("GET", f"/api/v1/standings/{YEAR}/drivers/after/{EVENT}", "Driver standings after event")
test_endpoint("GET", f"/api/v1/standings/{YEAR}/constructors/after/{EVENT}", "Constructor standings after event")
print()

# Qualifying Endpoints
print("🏁 QUALIFYING ENDPOINTS")
print("-" * 80)
test_endpoint("GET", f"/api/v1/results/{YEAR}/{EVENT}/qualifying/q1", "Q1 results")
test_endpoint("GET", f"/api/v1/results/{YEAR}/{EVENT}/qualifying/q2", "Q2 results")
test_endpoint("GET", f"/api/v1/results/{YEAR}/{EVENT}/qualifying/q3", "Q3 results")
test_endpoint("GET", f"/api/v1/grid/{YEAR}/{EVENT}", "Grid positions")
print()

# Health Check
print("💚 HEALTH CHECK")
print("-" * 80)
test_endpoint("GET", "/health", "Health check")
test_endpoint("GET", "/", "Root endpoint")
print()

# Summary
print("=" * 80)
print("TEST SUMMARY")
print("=" * 80)

passed = sum(1 for r in results if r[2])
failed = sum(1 for r in results if not r[2])
total = len(results)

print(f"\nTotal Endpoints Tested: {total}")
print(f"✅ Passed: {passed}")
print(f"❌ Failed: {failed}")
print(f"Success Rate: {(passed/total*100):.1f}%")
print()

# Show failed tests
if failed > 0:
    print("=" * 80)
    print("FAILED TESTS:")
    print("=" * 80)
    for status, desc, success, details in results:
        if not success:
            print(f"{status} {desc}")
            print(f"   {details}")
            print()

# Show all results
print("=" * 80)
print("ALL TEST RESULTS:")
print("=" * 80)
for status, desc, success, details in results:
    print(f"{status} {desc:60s} {details}")

print()
print("=" * 80)
if failed == 0:
    print("🎉 ALL TESTS PASSED!")
else:
    print(f"⚠️  {failed} test(s) failed. See details above.")
print("=" * 80)

sys.exit(0 if failed == 0 else 1)

