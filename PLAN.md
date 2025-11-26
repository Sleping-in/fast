# FastF1 API Deployment Plan

## Status: ✅ Completed
All planned features and additional requested features have been implemented.
- Core endpoints (Events, Sessions, Results, Laps, Telemetry) are implemented.
- Advanced features (Weather, Track Status, Pit Stops, Circuit Info, Race Control, Tyres, Standings, Gaps, Sectors) are implemented.
- Historical data via Ergast API is implemented.
- Deployment to Hugging Face Spaces is configured and verified.
- Comprehensive tests have been run and passed (with expected timeouts on first run).
- Final verification against FastF1 documentation completed.

## Overview
This project will create a REST API using FastAPI that exposes Formula 1 data from the FastF1 Python library, deployed on Railway.app. The API is designed to be consumed by a Swift iOS/macOS application.

## Project Structure
```
fastf1-api/
├── main.py              # FastAPI application entry point
├── api/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── events.py    # Event/session endpoints
│   │   ├── telemetry.py # Telemetry data endpoints
│   │   ├── laps.py      # Lap time endpoints
│   │   └── results.py   # Race results endpoints
│   └── models/
│       ├── __init__.py
│       └── schemas.py   # Pydantic models for responses
├── utils/
│   ├── __init__.py
│   └── cache.py         # Cache management utilities
├── requirements.txt     # Python dependencies
├── Procfile            # Railway deployment configuration
├── .env.example        # Example environment variables
├── .gitignore
└── README.md           # Project documentation
```

## API Endpoints Design

### 1. Event & Session Information
- `GET /api/v1/events/{year}` - List all events for a year
- `GET /api/v1/events/{year}/{event_name}` - Get specific event details
- `GET /api/v1/sessions/{year}/{event_name}/{session_type}` - Get session information
  - Session types: 'FP1', 'FP2', 'FP3', 'Q', 'R' (Race), 'S' (Sprint)

### 2. Race Results
- `GET /api/v1/results/{year}/{event_name}` - Get race results
- `GET /api/v1/results/{year}/{event_name}/qualifying` - Get qualifying results
- `GET /api/v1/results/{year}/{event_name}/sprint` - Get sprint results

### 3. Lap Times
- `GET /api/v1/laps/{year}/{event_name}` - Get all lap times for race
- `GET /api/v1/laps/{year}/{event_name}/{driver}` - Get lap times for specific driver
- `GET /api/v1/laps/{year}/{event_name}/fastest` - Get fastest lap information

### 4. Telemetry Data
- `GET /api/v1/telemetry/{year}/{event_name}/{driver}` - Get telemetry for driver
- `GET /api/v1/telemetry/{year}/{event_name}/{driver}/lap/{lap_number}` - Get telemetry for specific lap

### 5. Driver & Car Data
- `GET /api/v1/drivers/{year}` - List all drivers for a year
- `GET /api/v1/drivers/{year}/{event_name}` - Get drivers for specific event
- `GET /api/v1/car-data/{year}/{event_name}/{driver}` - Get car data (speed, throttle, brake, etc.)

## Technical Considerations

### FastF1 Library Usage
- FastF1 uses caching to store downloaded data (~50-100MB per session)
- Cache directory should be configured (default: `~/.fastf1/cache`)
- Sessions need to be loaded before accessing data: `session.load()`
- Data is returned as Pandas DataFrames, need to convert to JSON

### Caching Strategy
- FastF1 handles its own caching of downloaded data
- API-level caching can be added for frequently accessed endpoints
- Consider using Redis or in-memory caching for API responses
- Cache invalidation when new race data becomes available

### Data Serialization (Swift-Compatible)
- Convert Pandas DataFrames to JSON-compatible formats
- Use Pydantic models for response validation
- **ISO 8601 datetime format** - Swift's `ISO8601DateFormatter` compatible
- **Consistent number types** - Use proper int/float types (not strings)
- **Nullable fields** - Use `Optional` types properly (null in JSON)
- **Snake_case to camelCase** - Consider response alias for Swift conventions (or keep snake_case for consistency)
- Consider pagination for large datasets
- **Consistent response structure** - All responses follow same format for easy Swift Codable parsing

### Error Handling (Swift-Friendly)
- Handle missing sessions/events gracefully
- Return appropriate HTTP status codes
- **Consistent error response format**:
  ```json
  {
    "error": {
      "code": "SESSION_NOT_FOUND",
      "message": "Session not found for the specified parameters",
      "details": {}
    }
  }
  ```
- Provide meaningful error messages
- Handle FastF1 API errors (network issues, missing data)
- Use standard HTTP status codes (400, 404, 500, etc.)

### Performance Optimization
- Lazy loading of session data
- Background tasks for pre-loading popular sessions
- **Response compression** (gzip) - Important for mobile apps
- **CORS middleware** - For development/testing (if needed)
- Rate limiting (if needed)
- **Response caching headers** - Help Swift app cache responses

## Deployment to Hugging Face Spaces (Executed)

### Requirements
1. **requirements.txt** - All Python dependencies
2. **Dockerfile** - Container configuration
   ```dockerfile
   FROM python:3.9
   WORKDIR /code
   COPY ./requirements.txt /code/requirements.txt
   RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
   COPY . /code
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
   ```
3. **Environment Variables** (optional):
   - `FASTF1_CACHE_DIR` - Custom cache directory (set to `/tmp/fastf1_cache`)

### Hugging Face Configuration
- Docker SDK
- Port 7860 (standard for HF Spaces)
- Persistent storage not strictly required for cache (re-downloads on restart)

## Deployment to Railway.app (Alternative)

## Implementation Steps

1. **Setup Project Structure**
   - Create directory structure
   - Initialize Python package files
   - Create .gitignore

2. **Install Dependencies**
   - Create requirements.txt
   - Include: fastapi, uvicorn, fastf1, pandas, pydantic

3. **Implement Core API**
   - Create main FastAPI app
   - Implement basic endpoints
   - Add error handling
   - Add response models

4. **Add Advanced Features**
   - Implement telemetry endpoints
   - Add caching layer
   - Add data serialization utilities
   - Implement pagination

5. **Testing**
   - Test endpoints locally
   - Verify data serialization
   - Test error cases

6. **Deployment Preparation**
   - Create Procfile
   - Configure environment variables
   - Update README with deployment instructions

7. **Deploy to Railway**
   - Push to GitHub
   - Connect to Railway
   - Configure environment variables
   - Deploy and test

## Dependencies

### Core
- `fastapi` - Web framework
- `uvicorn[standard]` - ASGI server
- `fastf1` - F1 data library
- `pandas` - Data manipulation (dependency of fastf1)

### Optional/Recommended
- `pydantic` - Data validation (included with FastAPI)
- `python-multipart` - For file uploads (if needed)
- `python-dotenv` - Environment variable management
- `fastapi-cors` or `starlette` - CORS middleware (for development)

## Swift App Integration Considerations

### Response Format Standards
1. **Date/Time Format**: ISO 8601 with timezone (e.g., `"2024-03-10T14:00:00+00:00"`)
   - Swift can parse with `ISO8601DateFormatter` or `JSONDecoder.dateDecodingStrategy`
   
2. **Number Types**: 
   - Use proper numeric types (not strings)
   - Handle NaN/null values explicitly
   - Use `null` for missing optional values

3. **Response Structure**:
   - Consistent top-level structure
   - Use arrays for lists: `{"data": [...]}`
   - Use objects for single items: `{"data": {...}}`
   - Include metadata when useful: `{"data": ..., "meta": {...}}`

4. **Error Responses**:
   - Always return JSON, even for errors
   - Include error code and message
   - Use standard HTTP status codes

5. **Pagination** (for large datasets):
   ```json
   {
     "data": [...],
     "pagination": {
       "page": 1,
       "per_page": 50,
       "total": 100,
       "has_next": true
     }
   }
   ```

### Swift Codable Examples
The API responses will be designed to work seamlessly with Swift's `Codable` protocol:
```swift
// Example Swift struct
struct RaceResult: Codable {
    let position: Int
    let driver: String
    let team: String
    let time: String?
    let points: Double
    let fastestLap: Bool
}
```

### API Documentation
- FastAPI auto-generates OpenAPI/Swagger docs at `/docs`
- Can be used to generate Swift client code if needed
- Interactive API testing at `/docs` endpoint

## Notes
- FastF1 requires internet connection to download data initially
- Cache directory can grow large (consider cleanup strategies)
- Some historical data may not be available
- Real-time data availability depends on F1 official data release
- **Mobile-friendly**: Responses optimized for mobile network usage (compression, efficient JSON)

