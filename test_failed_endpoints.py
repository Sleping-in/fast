import requests
import sys
import json

BASE_URL = "http://localhost:8000"
YEAR = 2024
EVENT = "Qatar"
SESSION = "R"

def test_endpoint(url):
    print(f"Testing {url}...")
    try:
        response = requests.get(url, timeout=60)
        print(f"Status: {response.status_code}")
        try:
            data = response.json()
            print(json.dumps(data, indent=2))
        except:
            print(response.text)
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 50)

endpoints = [
    f"/api/v1/sectors/{YEAR}/{EVENT}/fastest/sector1?session_type={SESSION}",
    f"/api/v1/sectors/{YEAR}/{EVENT}/fastest/sector2?session_type={SESSION}",
    f"/api/v1/sectors/{YEAR}/{EVENT}/fastest/sector3?session_type={SESSION}",
    f"/api/v1/pit-stops/{YEAR}/{EVENT}/{SESSION}/fastest",
    f"/api/v1/pit-stops/{YEAR}/{EVENT}/{SESSION}/strategy",
    f"/api/v1/laps/{YEAR}/{EVENT}/personal-best?session_type={SESSION}",
    f"/api/v1/positions/{YEAR}/{EVENT}/{SESSION}/changes",
    f"/api/v1/positions/{YEAR}/{EVENT}/{SESSION}/overtakes"
]

print(f"Testing failed endpoints for {YEAR} {EVENT} {SESSION}")
print("=" * 50)

for endpoint in endpoints:
    test_endpoint(f"{BASE_URL}{endpoint}")
