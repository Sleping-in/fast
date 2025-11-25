import requests
import sys
import json

BASE_URL = "http://localhost:8000"
YEAR = 2024
EVENT = "Silverstone"
SESSION = "R"

endpoints = [
    f"/api/v1/events/{YEAR}/{EVENT}",
    f"/api/v1/laps/{YEAR}/{EVENT}/personal-best?session_type={SESSION}",
    f"/api/v1/positions/{YEAR}/{EVENT}/{SESSION}/changes",
    f"/api/v1/pit-stops/{YEAR}/{EVENT}/{SESSION}/fastest",
    f"/api/v1/sectors/{YEAR}/{EVENT}/fastest/sector1?session_type={SESSION}",
    f"/api/v1/results/{YEAR}/{EVENT}/sprint", # Expected 404
]

print(f"Debugging 404s for {YEAR} {EVENT}...\n")

for endpoint in endpoints:
    url = f"{BASE_URL}{endpoint}"
    print(f"GET {endpoint}")
    try:
        response = requests.get(url, timeout=60)
        print(f"Status: {response.status_code}")
        if response.status_code == 404:
            try:
                print(f"Response: {json.dumps(response.json(), indent=2)}")
            except:
                print(f"Response: {response.text}")
        elif response.status_code == 200:
            print("✅ Success (Unexpectedly?)")
        else:
            print(f"Status: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 40)
