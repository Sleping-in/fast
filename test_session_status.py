import requests
import sys

def test_session_status():
    url = "http://localhost:8000/api/v1/track-status/2023/Bahrain/R/session-status"
    try:
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            print("✅ Session Status Test Passed")
            print(response.json()['data'][:2]) # Print first 2 items
        else:
            print(f"❌ Session Status Test Failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Session Status Test Error: {e}")

if __name__ == "__main__":
    test_session_status()
