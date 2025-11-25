import requests
import sys
import time

BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "https://sleping-apex.hf.space"
YEAR = 2024
EVENT = "Silverstone"

print(f"Testing Circuit Info for {YEAR} {EVENT}...")
print("This may take up to 60 seconds if the server needs to download data...")

start_time = time.time()
try:
    url = f"{BASE_URL}/api/v1/circuits/{YEAR}/{EVENT}"
    print(f"Requesting: {url}")
    response = requests.get(url, timeout=120)
    elapsed = time.time() - start_time
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Time Taken: {elapsed:.2f} seconds")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Success!")
        print(f"Circuit Name: {data.get('meta', {}).get('event_name')}")
        # Print a snippet of data to prove it's real
        print("Data keys:", list(data.get('data', {}).keys())[:5])
    else:
        print("❌ Failed")
        print(response.text)

except Exception as e:
    print(f"\n❌ Error: {e}")
