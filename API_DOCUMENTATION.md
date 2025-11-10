# FastF1 API Documentation

**Base URL:** `https://angelic-unity-production.up.railway.app`  
**API Version:** v1  
**Documentation:** `/docs` (Interactive Swagger UI)

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Response Format](#response-format)
3. [Error Handling](#error-handling)
4. [Endpoints](#endpoints)
   - [Events](#events)
   - [Sessions](#sessions)
   - [Results](#results)
   - [Drivers](#drivers)
   - [Laps](#laps)
   - [Telemetry](#telemetry)
5. [Swift Integration](#swift-integration)
6. [Examples](#examples)

---

## Quick Start

All endpoints are accessible via HTTP GET requests. No authentication required.

```bash
# Health check
curl https://angelic-unity-production.up.railway.app/health

# Get events for 2025
curl https://angelic-unity-production.up.railway.app/api/v1/events/2025
```

---

## Response Format

All successful responses follow this structure:

```json
{
  "data": [...],
  "meta": {
    "year": 2025,
    "event_name": "Bahrain Grand Prix",
    "count": 20
  }
}
```

**Error responses:**
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {}
  }
}
```

---

## Error Handling

### HTTP Status Codes

- `200` - Success
- `400` - Bad Request (invalid parameters)
- `404` - Not Found (session/event doesn't exist)
- `500` - Internal Server Error

### Common Error Codes

- `EVENT_NOT_FOUND` - Event doesn't exist for the specified year
- `SESSION_NOT_FOUND` - Session data not available
- `DRIVER_NOT_FOUND` - Driver not found in session
- `INVALID_SESSION_TYPE` - Invalid session type (must be FP1, FP2, FP3, Q, R, S)

---

## Endpoints

### Events

#### Get All Events for a Year

```http
GET /api/v1/events/{year}
```

**Parameters:**
- `year` (path) - Year (e.g., 2024, 2025)

**Example:**
```bash
GET /api/v1/events/2025
```

**Response:**
```json
{
  "data": [
    {
      "event_name": "Bahrain Grand Prix",
      "event_date": "2025-04-13T00:00:00",
      "event_format": "conventional",
      "location": "Sakhir",
      "country": "Bahrain",
      "timezone": "",
      "round_number": 4
    }
  ],
  "meta": {
    "year": 2025,
    "count": 24
  }
}
```

---

#### Get Specific Event

```http
GET /api/v1/events/{year}/{event_name}
```

**Parameters:**
- `year` (path) - Year
- `event_name` (path) - Event name (partial match, e.g., "Bahrain" matches "Bahrain Grand Prix")

**Example:**
```bash
GET /api/v1/events/2025/Bahrain
```

---

### Sessions

#### Get Session Information

```http
GET /api/v1/sessions/{year}/{event_name}/{session_type}
```

**Parameters:**
- `year` (path) - Year
- `event_name` (path) - Event name
- `session_type` (path) - Session type: `FP1`, `FP2`, `FP3`, `Q`, `R`, `S`
  - `FP1`, `FP2`, `FP3` - Free Practice sessions
  - `Q` - Qualifying
  - `R` - Race
  - `S` - Sprint

**Example:**
```bash
GET /api/v1/sessions/2025/Bahrain/R
```

**Response:**
```json
{
  "data": {
    "session_name": "Race",
    "session_date": "2025-04-13T15:00:00",
    "session_type": "R",
    "event_name": "Bahrain Grand Prix",
    "year": 2025
  }
}
```

---

### Results

#### Get Race Results

```http
GET /api/v1/results/{year}/{event_name}
```

**Example:**
```bash
GET /api/v1/results/2025/Bahrain
```

**Response:**
```json
{
  "data": [
    {
      "DriverNumber": "81",
      "Abbreviation": "PIA",
      "FullName": "Oscar Piastri",
      "TeamName": "McLaren",
      "Position": 1.0,
      "Points": 25.0,
      "Time": "PT5739.435S",
      "Status": "Finished",
      "Laps": 57.0
    }
  ],
  "meta": {
    "year": 2025,
    "event_name": "Bahrain",
    "session_type": "Race",
    "count": 20
  }
}
```

---

#### Get Qualifying Results

```http
GET /api/v1/results/{year}/{event_name}/qualifying
```

**Example:**
```bash
GET /api/v1/results/2025/Bahrain/qualifying
```

**Response includes:** Q1, Q2, Q3 times, grid positions

---

#### Get Sprint Results

```http
GET /api/v1/results/{year}/{event_name}/sprint
```

**Example:**
```bash
GET /api/v1/results/2025/China/sprint
```

---

### Drivers

#### Get All Drivers for a Year

```http
GET /api/v1/drivers/{year}
```

**Example:**
```bash
GET /api/v1/drivers/2025
```

**Response:**
```json
{
  "data": [
    {
      "driver_number": 1,
      "abbreviation": "VER",
      "full_name": "Max Verstappen",
      "team_name": "Red Bull Racing",
      "country_code": "NED"
    }
  ],
  "meta": {
    "year": 2025,
    "count": 20
  }
}
```

---

#### Get Drivers for Specific Event

```http
GET /api/v1/drivers/{year}/{event_name}
```

**Example:**
```bash
GET /api/v1/drivers/2025/Bahrain
```

**Response includes:** Position and points for each driver

---

### Laps

#### Get All Laps

```http
GET /api/v1/laps/{year}/{event_name}?session_type={session_type}
```

**Parameters:**
- `year` (path) - Year
- `event_name` (path) - Event name
- `session_type` (query, optional) - Default: `R` (Race)

**Example:**
```bash
GET /api/v1/laps/2025/Bahrain?session_type=R
```

**Response includes:** Lap times, sectors, speeds, tyre compounds, positions

---

#### Get Fastest Lap

```http
GET /api/v1/laps/{year}/{event_name}/fastest?session_type={session_type}
```

**Example:**
```bash
GET /api/v1/laps/2025/Bahrain/fastest?session_type=R
```

**Response:**
```json
{
  "data": {
    "Driver": "PIA",
    "DriverNumber": "81",
    "LapTime": "PT1M35S",
    "LapNumber": 36.0,
    "Sector1Time": "PT30S",
    "Sector2Time": "PT41S",
    "Sector3Time": "PT23S",
    "Compound": "MEDIUM",
    "SpeedFL": 280.0
  },
  "meta": {
    "year": 2025,
    "event_name": "Bahrain",
    "session_type": "R"
  }
}
```

---

#### Get Driver-Specific Laps

```http
GET /api/v1/laps/{year}/{event_name}/{driver}?session_type={session_type}
```

**Parameters:**
- `driver` (path) - Driver abbreviation (e.g., `VER`) or driver number (e.g., `1`)

**Example:**
```bash
GET /api/v1/laps/2025/Bahrain/VER?session_type=R
GET /api/v1/laps/2025/Bahrain/1?session_type=R
```

---

### Telemetry

#### Get Driver Telemetry

```http
GET /api/v1/telemetry/{year}/{event_name}/{driver}?session_type={session_type}&lap={lap_number}
```

**Parameters:**
- `driver` (path) - Driver abbreviation or number
- `session_type` (query, optional) - Default: `R`
- `lap` (query, optional) - Specific lap number

**Example:**
```bash
# All telemetry for driver
GET /api/v1/telemetry/2025/Bahrain/VER?session_type=R

# Specific lap telemetry
GET /api/v1/telemetry/2025/Bahrain/VER?session_type=R&lap=10
```

**Response includes:** Speed, RPM, throttle, brake, DRS, position (X, Y, Z coordinates)

---

#### Get Car Data

```http
GET /api/v1/car-data/{year}/{event_name}/{driver}?session_type={session_type}
```

**Example:**
```bash
GET /api/v1/car-data/2025/Bahrain/VER?session_type=R
```

**Response includes:** RPM, speed, gear, throttle, brake, DRS

---

## Swift Integration

### Setup

```swift
import Foundation

let baseURL = "https://angelic-unity-production.up.railway.app"
```

### Response Models

```swift
struct APIResponse<T: Codable>: Codable {
    let data: T
    let meta: [String: Any]?
    
    enum CodingKeys: String, CodingKey {
        case data, meta
    }
    
    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        data = try container.decode(T.self, forKey: .data)
        meta = try? container.decode([String: Any].self, forKey: .meta)
    }
}

struct Event: Codable {
    let eventName: String
    let eventDate: String
    let location: String
    let country: String
    let roundNumber: Int?
    
    enum CodingKeys: String, CodingKey {
        case eventName = "event_name"
        case eventDate = "event_date"
        case location, country
        case roundNumber = "round_number"
    }
}

struct RaceResult: Codable {
    let driverNumber: String
    let abbreviation: String
    let fullName: String
    let teamName: String
    let position: Double
    let points: Double?
    let time: String?
    let status: String?
    
    enum CodingKeys: String, CodingKey {
        case driverNumber = "DriverNumber"
        case abbreviation = "Abbreviation"
        case fullName = "FullName"
        case teamName = "TeamName"
        case position = "Position"
        case points = "Points"
        case time = "Time"
        case status = "Status"
    }
}
```

### API Client

```swift
class FastF1API {
    private let baseURL = "https://angelic-unity-production.up.railway.app"
    
    private var decoder: JSONDecoder {
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        return decoder
    }
    
    // Get events for a year
    func getEvents(year: Int) async throws -> [Event] {
        let url = URL(string: "\(baseURL)/api/v1/events/\(year)")!
        let (data, _) = try await URLSession.shared.data(from: url)
        let response = try decoder.decode(APIResponse<[Event]>.self, from: data)
        return response.data
    }
    
    // Get race results
    func getRaceResults(year: Int, eventName: String) async throws -> [RaceResult] {
        let encodedName = eventName.addingPercentEncoding(withAllowedCharacters: .urlPathAllowed) ?? eventName
        let url = URL(string: "\(baseURL)/api/v1/results/\(year)/\(encodedName)")!
        let (data, _) = try await URLSession.shared.data(from: url)
        let response = try decoder.decode(APIResponse<[RaceResult]>.self, from: data)
        return response.data
    }
    
    // Get fastest lap
    func getFastestLap(year: Int, eventName: String, sessionType: String = "R") async throws -> [String: Any] {
        let encodedName = eventName.addingPercentEncoding(withAllowedCharacters: .urlPathAllowed) ?? eventName
        let url = URL(string: "\(baseURL)/api/v1/laps/\(year)/\(encodedName)/fastest?session_type=\(sessionType)")!
        let (data, _) = try await URLSession.shared.data(from: url)
        let json = try JSONSerialization.jsonObject(with: data) as? [String: Any]
        return json?["data"] as? [String: Any] ?? [:]
    }
}
```

### Usage Example

```swift
let api = FastF1API()

// Get 2025 events
let events = try await api.getEvents(year: 2025)

// Get race results
let results = try await api.getRaceResults(year: 2025, eventName: "Bahrain")

// Get fastest lap
let fastestLap = try await api.getFastestLap(year: 2025, eventName: "Bahrain")
```

---

## Examples

### Get Current Season Events

```bash
curl https://angelic-unity-production.up.railway.app/api/v1/events/2025
```

### Get Latest Race Results

```bash
curl https://angelic-unity-production.up.railway.app/api/v1/results/2025/Bahrain
```

### Get Driver's Best Lap

```bash
# Get all laps for driver
curl "https://angelic-unity-production.up.railway.app/api/v1/laps/2025/Bahrain/VER?session_type=R"

# Get fastest lap overall
curl "https://angelic-unity-production.up.railway.app/api/v1/laps/2025/Bahrain/fastest?session_type=R"
```

### Get Telemetry for Analysis

```bash
# Full race telemetry
curl "https://angelic-unity-production.up.railway.app/api/v1/telemetry/2025/Bahrain/VER?session_type=R"

# Specific lap
curl "https://angelic-unity-production.up.railway.app/api/v1/telemetry/2025/Bahrain/VER?session_type=R&lap=10"
```

---

## Notes

- **Date Format:** All dates are in ISO 8601 format (e.g., `2025-04-13T15:00:00`)
- **Time Format:** Lap times use ISO 8601 duration format (e.g., `PT1M35S` = 1 minute 35 seconds)
- **Event Names:** Use partial names (e.g., "Bahrain" matches "Bahrain Grand Prix")
- **Driver Identifiers:** Use abbreviation (e.g., `VER`) or driver number (e.g., `1`)
- **Caching:** First request may be slower as data is downloaded and cached
- **Rate Limiting:** No rate limits currently, but be respectful

---

## Interactive Documentation

Visit `/docs` for interactive Swagger UI documentation:
```
https://angelic-unity-production.up.railway.app/docs
```

---

## Support

For issues or questions, check the repository or API documentation at `/docs`.

