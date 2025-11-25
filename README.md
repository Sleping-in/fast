---
title: Apex
emoji: 🏎️
colorFrom: red
colorTo: gray
sdk: docker
pinned: false
---

# FastF1 API

A REST API for Formula 1 data using the FastF1 Python library. Optimized for Swift iOS/macOS app consumption and deployed on Hugging Face Spaces.

## Features

- 🏎️ Complete Formula 1 data access (events, sessions, results, lap times, telemetry)
- 📱 Swift-optimized JSON responses with ISO 8601 dates
- 🚀 FastAPI with automatic OpenAPI documentation
- ☁️ Hugging Face Spaces deployment ready (Docker)
- 🔄 Built-in caching for performance
- 📊 Consistent error handling and response formats

## API Endpoints

### Events & Sessions
- `GET /api/v1/events/{year}` - List all events for a year
- `GET /api/v1/events/{year}/{event_name}` - Get specific event details
- `GET /api/v1/sessions/{year}/{event_name}/{session_type}` - Get session information
  - Session types: `FP1`, `FP2`, `FP3`, `Q` (Qualifying), `R` (Race), `S` (Sprint)

### Results
- `GET /api/v1/results/{year}/{event_name}` - Get race results
- `GET /api/v1/results/{year}/{event_name}/qualifying` - Get qualifying results
- `GET /api/v1/results/{year}/{event_name}/sprint` - Get sprint results

### Lap Times
- `GET /api/v1/laps/{year}/{event_name}` - Get all lap times
- `GET /api/v1/laps/{year}/{event_name}/{driver}` - Get lap times for specific driver
- `GET /api/v1/laps/{year}/{event_name}/fastest` - Get fastest lap information

### Telemetry
- `GET /api/v1/telemetry/{year}/{event_name}/{driver}` - Get telemetry for driver
- `GET /api/v1/telemetry/{year}/{event_name}/{driver}?lap={lap_number}` - Get telemetry for specific lap
- `GET /api/v1/car-data/{year}/{event_name}/{driver}` - Get car data (speed, throttle, brake, etc.)

### Drivers
- `GET /api/v1/drivers/{year}` - List all drivers for a year
- `GET /api/v1/drivers/{year}/{event_name}` - Get drivers for specific event

## Local Development

### Prerequisites
- Python 3.8 or higher
- pip

### Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd fastf1-api
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the development server:
```bash
python3 main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Note for macOS:** Use `python3` instead of `python` if `python` points to Python 2.x.

5. Access the API:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- OpenAPI schema: http://localhost:8000/openapi.json

## Deployment to Railway.app

### Method 1: Deploy from GitHub

1. **Push your code to GitHub:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. **Create Railway project:**
   - Go to [Railway.app](https://railway.app)
   - Sign up or log in
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure environment variables (optional):**
   - In Railway dashboard, go to Settings → Variables
   - Add `FASTF1_CACHE_DIR` if you want a custom cache location
   - Add `LOG_LEVEL` for logging configuration

4. **Deploy:**
   - Railway will automatically detect the `Procfile` and `requirements.txt`
   - The app will build and deploy automatically
   - Railway will provide a public URL for your API

### Method 2: Deploy using Railway CLI

1. **Install Railway CLI:**
```bash
npm i -g @railway/cli
```

2. **Login and initialize:**
```bash
railway login
railway init
```

3. **Deploy:**
```bash
railway up
```

## Deployment to Hugging Face Spaces

1. **Create a new Space:**
   - Go to [Hugging Face Spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Enter a name for your space
   - Select "Docker" as the SDK
   - Choose "Blank" as the template

2. **Push your code:**
   - Clone the repository provided by Hugging Face
   - Copy your project files into the cloned repository
   - Push the changes:
     ```bash
     git add .
     git commit -m "Initial commit"
     git push
     ```
   - Alternatively, you can connect your GitHub repository directly if you have one.

3. **Configuration:**
   - The `Dockerfile` is already configured to run the application on port 7860.
   - The cache directory is set to `/tmp/fastf1_cache` which is writable in the Space environment.

## Environment Variables

Optional environment variables:

- `FASTF1_CACHE_DIR` - Custom directory for FastF1 cache (default: `~/.fastf1/cache`)
- `LOG_LEVEL` - Logging level (default: INFO)
- `PORT` - Port number (Railway sets this automatically)

## Swift Integration

The API is designed to work seamlessly with Swift's `Codable` protocol:

### Example Swift Code

```swift
import Foundation

struct RaceResult: Codable {
    let position: Int?
    let driverNumber: Int?
    let abbreviation: String?
    let fullName: String?
    let teamName: String?
    let points: Double?
    let time: String?
    let status: String?
    let fastestLap: Bool?
}

struct APIResponse: Codable {
    let data: [RaceResult]
    let meta: [String: Any]?
}

// Fetch race results
func fetchRaceResults(year: Int, eventName: String) async throws -> [RaceResult] {
    let url = URL(string: "https://sleping-apex.hf.space/api/v1/results/\(year)/\(eventName)")!
    let (data, _) = try await URLSession.shared.data(from: url)
    
    let decoder = JSONDecoder()
    decoder.dateDecodingStrategy = .iso8601
    
    let response = try decoder.decode(APIResponse.self, from: data)
    return response.data
}
```

### Date Handling

All dates are returned in ISO 8601 format. Configure your `JSONDecoder`:

```swift
let decoder = JSONDecoder()
decoder.dateDecodingStrategy = .iso8601
```

## Response Format

All responses follow a consistent format:

### Success Response
```json
{
  "data": [...],
  "meta": {
    "year": 2024,
    "event_name": "Bahrain Grand Prix",
    "count": 20
  }
}
```

### Error Response
```json
{
  "error": {
    "code": "SESSION_NOT_FOUND",
    "message": "Session not found for the specified parameters",
    "details": {}
  }
}
```

## API Documentation

FastAPI automatically generates interactive API documentation:
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`

## Notes

- FastF1 requires an internet connection to download data initially
- Cache directory can grow large (~50-100MB per session)
- Some historical data may not be available
- Real-time data availability depends on F1 official data release
- First request for a session may be slower as data is downloaded and cached

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

