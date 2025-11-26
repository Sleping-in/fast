# FastF1 API Documentation

**Base URL:** `https://sleping-apex.hf.space`  
**API Version:** v1  
**Interactive Documentation:** `/docs` (Swagger UI)

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
   - [Weather](#weather)
   - [Track Status](#track-status)
   - [Positions](#positions)
   - [Pit Stops](#pit-stops)
   - [Circuits](#circuits)
   - [Race Control](#race-control)
   - [Sectors](#sectors)
   - [Gaps](#gaps)
   - [Tyres](#tyres)
   - [Teams](#teams)
   - [Standings](#standings)
   - [Historical Data](#historical-data)
5. [Swift Integration](#swift-integration)
6. [Examples](#examples)

---

## Quick Start

All endpoints are accessible via HTTP GET requests. No authentication required.

```bash
# Health check
curl https://sleping-apex.hf.space/health

# Get events for 2025
curl https://sleping-apex.hf.space/api/v1/events/2025
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
- `404` - Not Found (session/event doesn't exist or data not available)
- `500` - Internal Server Error

### Common Error Codes

- `EVENT_NOT_FOUND` - Event doesn't exist for the specified year
- `SESSION_NOT_FOUND` - Session data not available
- `DRIVER_NOT_FOUND` - Driver not found in session
- `INVALID_SESSION_TYPE` - Invalid session type (must be FP1, FP2, FP3, Q, R, S, SQ)
- `LAPS_NOT_FOUND` - No lap data available
- `TELEMETRY_NOT_FOUND` - No telemetry data available
- `WEATHER_NOT_FOUND` - No weather data available
- `TRACK_STATUS_NOT_FOUND` - No track status data available

**Note:** A `404` response doesn't always mean an error - it may indicate that data isn't available for that specific session (e.g., no weather data, no pit stops).

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

#### Get Upcoming Events

```http
GET /api/v1/events/upcoming
```

**Description:** Get upcoming events for the current year.

**Example:**
```bash
GET /api/v1/events/upcoming
```

---

#### Get Past Events

```http
GET /api/v1/events/{year}/past
```

**Description:** Get past events for a specific year.

**Example:**
```bash
GET /api/v1/events/2025/past
```

---

#### Get Event by Round

```http
GET /api/v1/events/{year}/round/{round_number}
```

**Description:** Get event by round number.

**Example:**
```bash
GET /api/v1/events/2025/round/1
```

---

#### Get Events by Country

```http
GET /api/v1/events/{year}/country/{country}
```

**Description:** Get events by country.

**Example:**
```bash
GET /api/v1/events/2025/country/Bahrain
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
- `session_type` (path) - Session type: `FP1`, `FP2`, `FP3`, `Q`, `R`, `S`, `SQ`
  - `FP1`, `FP2`, `FP3` - Free Practice sessions
  - `Q` - Qualifying
  - `R` - Race
  - `S` - Sprint
  - `SQ` - Sprint Qualifying (Sprint Shootout)

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

#### Get Q1 Results

```http
GET /api/v1/results/{year}/{event_name}/qualifying/q1
```

**Description:** Get Q1 qualifying session results only.

**Example:**
```bash
GET /api/v1/results/2025/Bahrain/qualifying/q1
```

---

#### Get Q2 Results

```http
GET /api/v1/results/{year}/{event_name}/qualifying/q2
```

**Description:** Get Q2 qualifying session results only.

**Example:**
```bash
GET /api/v1/results/2025/Bahrain/qualifying/q2
```

---

#### Get Q3 Results

```http
GET /api/v1/results/{year}/{event_name}/qualifying/q3
```

**Description:** Get Q3 qualifying session results only.

**Example:**
```bash
GET /api/v1/results/2025/Bahrain/qualifying/q3
```

---

#### Get Grid Positions

```http
GET /api/v1/grid/{year}/{event_name}
```

**Description:** Get starting grid positions for the race.

**Example:**
```bash
GET /api/v1/grid/2025/Bahrain
```

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

#### Get Sprint Qualifying Results

```http
GET /api/v1/results/{year}/{event_name}/sprint-qualifying
```

**Description:** Get sprint qualifying (sprint shootout) results. Sprint qualifying determines the grid for the sprint race.

**Example:**
```bash
GET /api/v1/results/2025/China/sprint-qualifying
```

**Note:** Sprint qualifying is available at select events. In 2025, sprint weekends include: China, Miami, Belgium, USA, Brazil, and Qatar.

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
GET /api/v1/laps/{year}/{event_name}?session_type={session_type}&quicklaps={bool}&compound={compound}&exclude_pits={bool}&track_status={status}&include_deleted={bool}
```

**Parameters:**
- `year` (path) - Year
- `event_name` (path) - Event name
- `session_type` (query, optional) - Default: `R` (Race). Options: `FP1`, `FP2`, `FP3`, `Q`, `R`, `S`, `SQ`
- `quicklaps` (query, optional) - Filter quick laps only (exclude in/out laps). Default: `false`
- `compound` (query, optional) - Filter by tyre compound: `SOFT`, `MEDIUM`, `HARD`, etc.
- `exclude_pits` (query, optional) - Exclude pit in/out laps. Default: `false`
- `track_status` (query, optional) - Filter by track status (1=clear, 2=yellow, etc.)
- `include_deleted` (query, optional) - Include deleted/invalid laps. Default: `false`

**Example:**
```bash
# All laps
GET /api/v1/laps/2025/Bahrain?session_type=R

# Quick laps only
GET /api/v1/laps/2025/Bahrain?session_type=R&quicklaps=true

# Laps on soft tyres
GET /api/v1/laps/2025/Bahrain?session_type=R&compound=SOFT

# Exclude pit stops
GET /api/v1/laps/2025/Bahrain?session_type=R&exclude_pits=true
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

#### Get Personal Best Laps

```http
GET /api/v1/laps/{year}/{event_name}/personal-best?session_type={session_type}
```

**Description:** Get personal best lap for each driver.

**Example:**
```bash
GET /api/v1/laps/2025/Bahrain/personal-best?session_type=R
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

**Response includes:** Speed, RPM, throttle, brake, DRS, position (X, Y, Z coordinates), time

---

#### Get DRS Data

```http
GET /api/v1/telemetry/{year}/{event_name}/{driver}/drs?session_type={session_type}&lap={lap_number}
```

**Description:** Get DRS activation data only.

**Example:**
```bash
GET /api/v1/telemetry/2025/Bahrain/VER/drs?session_type=R
```

---

#### Get Speed Data

```http
GET /api/v1/telemetry/{year}/{event_name}/{driver}/speed?session_type={session_type}&lap={lap_number}
```

**Description:** Get speed data only.

**Example:**
```bash
GET /api/v1/telemetry/2025/Bahrain/VER/speed?session_type=R
```

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

### Weather

#### Get Weather Data

```http
GET /api/v1/weather/{year}/{event_name}/{session_type}?time={timestamp}
```

**Parameters:**
- `year` (path) - Year
- `event_name` (path) - Event name
- `session_type` (path) - Session type: `FP1`, `FP2`, `FP3`, `Q`, `R`, `S`, `SQ`
- `time` (query, optional) - Specific timestamp (ISO 8601 format)

**Example:**
```bash
# All weather data
GET /api/v1/weather/2025/Bahrain/R

# Weather at specific time
GET /api/v1/weather/2025/Bahrain/R?time=2025-04-13T15:30:00
```

**Response includes:** Air temperature, track temperature, humidity, wind speed, wind direction, pressure

---

#### Get Weather Summary

```http
GET /api/v1/weather/{year}/{event_name}/{session_type}/summary
```

**Description:** Get weather summary statistics (min/max/average).

**Example:**
```bash
GET /api/v1/weather/2025/Bahrain/R/summary
```

**Response:**
```json
{
  "data": {
    "AirTemp": {
      "min": 25.0,
      "max": 28.0,
      "mean": 26.5,
      "std": 0.8
    },
    "TrackTemp": {
      "min": 35.0,
      "max": 42.0,
      "mean": 38.5,
      "std": 1.2
    }
  }
}
```

---

### Track Status

#### Get Track Status

```http
GET /api/v1/track-status/{year}/{event_name}/{session_type}
```

**Description:** Get track status data (flags, safety car, VSC, etc.).

**Parameters:**
- `year` (path) - Year
- `event_name` (path) - Event name
- `session_type` (path) - Session type: `FP1`, `FP2`, `FP3`, `Q`, `R`, `S`, `SQ`

**Example:**
```bash
GET /api/v1/track-status/2025/Bahrain/R
```

**Response includes:** Status changes, flag types, timestamps, status messages

---

#### Get Safety Car Periods

```http
GET /api/v1/track-status/{year}/{event_name}/{session_type}/safety-car
```

**Example:**
```bash
GET /api/v1/track-status/2025/Bahrain/R/safety-car
```

---

#### Get Virtual Safety Car Periods

```http
GET /api/v1/track-status/{year}/{event_name}/{session_type}/vsc
```

**Example:**
```bash
GET /api/v1/track-status/2025/Bahrain/R/vsc
```

---

#### Get Red Flag Periods

```http
GET /api/v1/track-status/{year}/{event_name}/{session_type}/red-flags
```

**Example:**
```bash
GET /api/v1/track-status/2025/Bahrain/R/red-flags
```

---

#### Get Yellow Flag Periods

```http
GET /api/v1/track-status/{year}/{event_name}/{session_type}/yellow-flags
```

**Example:**
```bash
GET /api/v1/track-status/2025/Bahrain/R/yellow-flags
```

---

### Positions

#### Get Position Data

```http
GET /api/v1/positions/{year}/{event_name}/{session_type}?time={timestamp}
```

**Description:** Get real-time position data for all drivers.

**Parameters:**
- `year` (path) - Year
- `event_name` (path) - Event name
- `session_type` (path) - Session type: `FP1`, `FP2`, `FP3`, `Q`, `R`, `S`, `SQ`
- `time` (query, optional) - Specific timestamp (ISO 8601 format)

**Example:**
```bash
# All position data
GET /api/v1/positions/2025/Bahrain/R

# Position at specific time
GET /api/v1/positions/2025/Bahrain/R?time=2025-04-13T15:30:00
```

---

#### Get Driver Positions

```http
GET /api/v1/positions/{year}/{event_name}/{session_type}/{driver}
```

**Description:** Get position data for a specific driver.

**Example:**
```bash
GET /api/v1/positions/2025/Bahrain/R/VER
```

---

#### Get Position Changes

```http
GET /api/v1/positions/{year}/{event_name}/{session_type}/changes
```

**Description:** Get all position changes during the session.

**Example:**
```bash
GET /api/v1/positions/2025/Bahrain/R/changes
```

**Response includes:** Driver, lap, previous position, current position, change

---

#### Get Overtakes

```http
GET /api/v1/positions/{year}/{event_name}/{session_type}/overtakes
```

**Description:** Get all overtakes (position gains).

**Example:**
```bash
GET /api/v1/positions/2025/Bahrain/R/overtakes
```

---

### Pit Stops

#### Get Pit Stops

```http
GET /api/v1/pit-stops/{year}/{event_name}/{session_type}?include_duration={bool}
```

**Parameters:**
- `year` (path) - Year
- `event_name` (path) - Event name
- `session_type` (path) - Session type: `FP1`, `FP2`, `FP3`, `Q`, `R`, `S`, `SQ`
- `include_duration` (query, optional) - Include pit stop duration. Default: `false`

**Example:**
```bash
# All pit stops
GET /api/v1/pit-stops/2025/Bahrain/R

# With duration
GET /api/v1/pit-stops/2025/Bahrain/R?include_duration=true
```

**Response includes:** Pit in time, pit out time, lap number, duration (if requested)

---

#### Get Driver Pit Stops

```http
GET /api/v1/pit-stops/{year}/{event_name}/{session_type}/{driver}?include_duration={bool}
```

**Example:**
```bash
GET /api/v1/pit-stops/2025/Bahrain/R/VER?include_duration=true
```

---

#### Get Fastest Pit Stop

```http
GET /api/v1/pit-stops/{year}/{event_name}/{session_type}/fastest
```

**Description:** Get the fastest pit stop in the session.

**Example:**
```bash
GET /api/v1/pit-stops/2025/Bahrain/R/fastest
```

---

#### Get Pit Stop Strategy

```http
GET /api/v1/pit-stops/{year}/{event_name}/{session_type}/strategy
```

**Description:** Get pit stop strategy analysis for all drivers.

**Example:**
```bash
GET /api/v1/pit-stops/2025/Bahrain/R/strategy
```

**Response includes:** Driver, total pit stops, pit stop details (lap, times, compound changes)

---

### Circuits

#### Get Circuit Information

```http
GET /api/v1/circuits/{year}/{event_name}
```

**Description:** Get circuit layout, corner numbers, marshal sectors, track length.

**Example:**
```bash
GET /api/v1/circuits/2025/Bahrain
```

**Response includes:** Track layout, corner numbers, marshal sectors, track length, coordinates

---

#### Get DRS Zones

```http
GET /api/v1/circuits/{year}/{event_name}/drs-zones
```

**Description:** Get DRS zone locations.

**Example:**
```bash
GET /api/v1/circuits/2025/Bahrain/drs-zones
```

---

#### Get Track Markers

```http
GET /api/v1/circuits/{year}/{event_name}/markers
```

**Description:** Get track markers (corners, marshal sectors, marshal lights).

**Example:**
```bash
GET /api/v1/circuits/2025/Bahrain/markers
```

---

#### Get Corners

```http
GET /api/v1/circuits/{year}/{event_name}/corners
```

**Description:** Get corner information.

**Example:**
```bash
GET /api/v1/circuits/2025/Bahrain/corners
```

---

#### Get Marshal Sectors

```http
GET /api/v1/circuits/{year}/{event_name}/marshal-sectors
```

**Description:** Get marshal sector information.

**Example:**
```bash
GET /api/v1/circuits/2025/Bahrain/marshal-sectors
```

---

### Race Control

#### Get Race Control Messages

```http
GET /api/v1/race-control/{year}/{event_name}/{session_type}?category={category}
```

**Description:** Get race control messages (penalties, investigations, announcements).

**Parameters:**
- `year` (path) - Year
- `event_name` (path) - Event name
- `session_type` (path) - Session type: `FP1`, `FP2`, `FP3`, `Q`, `R`, `S`, `SQ`
- `category` (query, optional) - Filter by category (penalty, investigation, etc.)

**Example:**
```bash
# All messages
GET /api/v1/race-control/2025/Bahrain/R

# Only penalties
GET /api/v1/race-control/2025/Bahrain/R?category=penalty
```

**Response includes:** Messages, timestamps, categories

---

#### Get Penalties

```http
GET /api/v1/race-control/{year}/{event_name}/{session_type}/penalties
```

**Description:** Get all penalties issued.

**Example:**
```bash
GET /api/v1/race-control/2025/Bahrain/R/penalties
```

---

#### Get Investigations

```http
GET /api/v1/race-control/{year}/{event_name}/{session_type}/investigations
```

**Description:** Get all investigations.

**Example:**
```bash
GET /api/v1/race-control/2025/Bahrain/R/investigations
```

---

### Sectors

#### Get All Sector Times

```http
GET /api/v1/sectors/{year}/{event_name}/{session_type}
```

**Description:** Get all sector times for a session.

**Parameters:**
- `year` (path) - Year
- `event_name` (path) - Event name
- `session_type` (path) - Session type: `FP1`, `FP2`, `FP3`, `Q`, `R`, `S`, `SQ`

**Example:**
```bash
GET /api/v1/sectors/2025/Bahrain/R
```

**Response includes:** Sector1Time, Sector2Time, Sector3Time for each lap

---

#### Get Driver Sector Times

```http
GET /api/v1/sectors/{year}/{event_name}/{session_type}/{driver}
```

**Example:**
```bash
GET /api/v1/sectors/2025/Bahrain/R/VER
```

---

#### Get Fastest Sector 1

```http
GET /api/v1/sectors/{year}/{event_name}/fastest/sector1?session_type={session_type}
```

**Example:**
```bash
GET /api/v1/sectors/2025/Bahrain/fastest/sector1?session_type=R
```

---

#### Get Fastest Sector 2

```http
GET /api/v1/sectors/{year}/{event_name}/fastest/sector2?session_type={session_type}
```

**Example:**
```bash
GET /api/v1/sectors/2025/Bahrain/fastest/sector2?session_type=R
```

---

#### Get Fastest Sector 3

```http
GET /api/v1/sectors/{year}/{event_name}/fastest/sector3?session_type={session_type}
```

**Example:**
```bash
GET /api/v1/sectors/2025/Bahrain/fastest/sector3?session_type=R
```

---

### Gaps

#### Get Gaps to Leader

```http
GET /api/v1/gaps/{year}/{event_name}/{session_type}?lap={lap_number}
```

**Description:** Get gap to leader for all drivers.

**Parameters:**
- `year` (path) - Year
- `event_name` (path) - Event name
- `session_type` (path) - Session type: `FP1`, `FP2`, `FP3`, `Q`, `R`, `S`, `SQ`
- `lap` (query, optional) - Specific lap number

**Example:**
```bash
# All gaps
GET /api/v1/gaps/2025/Bahrain/R

# Gaps at specific lap
GET /api/v1/gaps/2025/Bahrain/R?lap=10
```

**Response includes:** Driver, lap, position, gap_to_leader_seconds

---

#### Get Driver Gaps

```http
GET /api/v1/gaps/{year}/{event_name}/{session_type}/{driver}
```

**Description:** Get gap to leader for a specific driver.

**Example:**
```bash
GET /api/v1/gaps/2025/Bahrain/R/VER
```

---

#### Get Gap to Driver Ahead

```http
GET /api/v1/gaps/{year}/{event_name}/{session_type}/{driver}/ahead
```

**Description:** Get gap to the driver ahead.

**Example:**
```bash
GET /api/v1/gaps/2025/Bahrain/R/VER/ahead
```

---

#### Get Gap to Driver Behind

```http
GET /api/v1/gaps/{year}/{event_name}/{session_type}/{driver}/behind
```

**Description:** Get gap to the driver behind.

**Example:**
```bash
GET /api/v1/gaps/2025/Bahrain/R/VER/behind
```

---

### Tyres

#### Get Tyre Compounds Used

```http
GET /api/v1/tyres/{year}/{event_name}/{session_type}/compounds
```

**Description:** Get list of tyre compounds used in the session.

**Example:**
```bash
GET /api/v1/tyres/2025/Bahrain/R/compounds
```

**Response:**
```json
{
  "data": {
    "compounds": ["SOFT", "MEDIUM", "HARD"]
  },
  "meta": {
    "year": 2025,
    "event_name": "Bahrain",
    "session_type": "R",
    "count": 3
  }
}
```

---

#### Get Tyre Strategy

```http
GET /api/v1/tyres/{year}/{event_name}/{session_type}/strategy
```

**Description:** Get tyre strategy analysis for all drivers.

**Example:**
```bash
GET /api/v1/tyres/2025/Bahrain/R/strategy
```

**Response includes:** Driver, total stints, stint details (compound, start lap, end lap, laps, average tyre life)

---

#### Get Driver Stints

```http
GET /api/v1/tyres/{year}/{event_name}/{session_type}/{driver}/stints
```

**Description:** Get stint information for a specific driver.

**Example:**
```bash
GET /api/v1/tyres/2025/Bahrain/R/VER/stints
```

---

#### Get Tyre Life Analysis

```http
GET /api/v1/tyres/{year}/{event_name}/{session_type}/life-analysis
```

**Description:** Get tyre life vs performance analysis.

**Example:**
```bash
GET /api/v1/tyres/2025/Bahrain/R/life-analysis
```

**Response includes:** Driver, average tyre life, average lap time, laps analyzed

---

### Teams

#### Get All Teams

```http
GET /api/v1/teams/{year}
```

**Description:** Get all teams for a year.

**Example:**
```bash
GET /api/v1/teams/2025
```

**Response includes:** Team name, team color

---

#### Get Event Teams

```http
GET /api/v1/teams/{year}/{event_name}
```

**Description:** Get teams for a specific event.

**Example:**
```bash
GET /api/v1/teams/2025/Bahrain
```

---

#### Get Team Results

```http
GET /api/v1/teams/{year}/{team_name}/results
```

**Description:** Get results for a specific team across all events in a year.

**Example:**
```bash
GET /api/v1/teams/2025/McLaren/results
```

**Response includes:** Event name, driver, position, points for each race

**Note:** This endpoint may take longer to respond as it processes all events for the year.

---

### Standings

#### Get Driver Standings

```http
GET /api/v1/standings/{year}/drivers
```

**Description:** Get driver championship standings for a year.

**Example:**
```bash
GET /api/v1/standings/2025/drivers
```

**Response:**
```json
{
  "data": [
    {
      "driver": "NOR",
      "full_name": "Lando Norris",
      "team": "McLaren",
      "points": 382.0,
      "wins": 7,
      "podiums": 18,
      "position": 1
    }
  ],
  "meta": {
    "year": 2025,
    "count": 21
  }
}
```

**Note:** This endpoint may take longer to respond (30-60 seconds) as it processes all events for the year.

---

#### Get Constructor Standings

```http
GET /api/v1/standings/{year}/constructors
```

**Description:** Get constructor championship standings for a year.

**Example:**
```bash
GET /api/v1/standings/2025/constructors
```

**Response:**
```json
{
  "data": [
    {
      "team": "McLaren",
      "points": 739.0,
      "wins": 14,
      "position": 1
    }
  ],
  "meta": {
    "year": 2025,
    "count": 10
  }
}
```

**Note:** This endpoint may take longer to respond (30-60 seconds) as it processes all events for the year.

---

#### Get Driver Standings After Event

```http
GET /api/v1/standings/{year}/drivers/after/{event_name}
```

**Description:** Get driver standings after a specific event.

**Example:**
```bash
GET /api/v1/standings/2025/drivers/after/Bahrain
```

---

#### Get Constructor Standings After Event

```http
GET /api/v1/standings/{year}/constructors/after/{event_name}
```

**Description:** Get constructor standings after a specific event.

**Example:**
```bash
GET /api/v1/standings/2025/constructors/after/Bahrain
```

---

### Historical Data

#### Get Historical Events

```http
GET /api/v1/historical/{year}/events
```

**Description:** Get historical events (races) for a specific year using Ergast API (pre-2018 supported).

**Example:**
```bash
GET /api/v1/historical/2010/events
```

---

#### Get Historical Results

```http
GET /api/v1/historical/{year}/results?round={round}&driver={driver}
```

**Description:** Get historical race results.

**Parameters:**
- `year` (path) - Year
- `round` (query, optional) - Round number
- `driver` (query, optional) - Driver ID

**Example:**
```bash
GET /api/v1/historical/2010/results?round=1
```

---

#### Get Historical Drivers

```http
GET /api/v1/historical/{year}/drivers?round={round}
```

**Description:** Get historical drivers.

**Example:**
```bash
GET /api/v1/historical/2010/drivers
```

---

#### Get Historical Constructors

```http
GET /api/v1/historical/{year}/constructors?round={round}
```

**Description:** Get historical constructors.

**Example:**
```bash
GET /api/v1/historical/2010/constructors
```

---

#### Get Historical Driver Standings

```http
GET /api/v1/historical/{year}/standings/drivers?round={round}
```

**Description:** Get historical driver standings.

**Example:**
```bash
GET /api/v1/historical/2010/standings/drivers
```

---

#### Get Historical Constructor Standings

```http
GET /api/v1/historical/{year}/standings/constructors?round={round}
```

**Description:** Get historical constructor standings.

**Example:**
```bash
GET /api/v1/historical/2010/standings/constructors
```

---

## Swift Integration

### Setup

```swift
import Foundation

let baseURL = "https://sleping-apex.hf.space"
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
    let position: Double?
    let driverNumber: String?
    let abbreviation: String?
    let fullName: String?
    let teamName: String?
    let points: Double?
    let time: String?
    let status: String?
    
    enum CodingKeys: String, CodingKey {
        case position = "Position"
        case driverNumber = "DriverNumber"
        case abbreviation = "Abbreviation"
        case fullName = "FullName"
        case teamName = "TeamName"
        case points = "Points"
        case time = "Time"
        case status = "Status"
    }
}
```

### API Client

```swift
class FastF1API {
    private let baseURL = "https://sleping-apex.hf.space"
    
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
    
    // Get weather data
    func getWeather(year: Int, eventName: String, sessionType: String) async throws -> [[String: Any]] {
        let encodedName = eventName.addingPercentEncoding(withAllowedCharacters: .urlPathAllowed) ?? eventName
        let url = URL(string: "\(baseURL)/api/v1/weather/\(year)/\(encodedName)/\(sessionType)")!
        let (data, _) = try await URLSession.shared.data(from: url)
        let json = try JSONSerialization.jsonObject(with: data) as? [String: Any]
        return json?["data"] as? [[String: Any]] ?? []
    }
    
    // Get standings
    func getDriverStandings(year: Int) async throws -> [[String: Any]] {
        let url = URL(string: "\(baseURL)/api/v1/standings/\(year)/drivers")!
        let (data, _) = try await URLSession.shared.data(from: url)
        let json = try JSONSerialization.jsonObject(with: data) as? [String: Any]
        return json?["data"] as? [[String: Any]] ?? []
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

// Get weather
let weather = try await api.getWeather(year: 2025, eventName: "Bahrain", sessionType: "R")

// Get standings
let standings = try await api.getDriverStandings(year: 2025)
```

---

## Examples

### Get Current Season Events

```bash
curl https://sleping-apex.hf.space/api/v1/events/2025
```

### Get Latest Race Results

```bash
curl https://sleping-apex.hf.space/api/v1/results/2025/Bahrain
```

### Get Qualifying Q1/Q2/Q3 Results

```bash
curl https://sleping-apex.hf.space/api/v1/results/2025/Bahrain/qualifying/q1
curl https://sleping-apex.hf.space/api/v1/results/2025/Bahrain/qualifying/q2
curl https://sleping-apex.hf.space/api/v1/results/2025/Bahrain/qualifying/q3
```

### Get Grid Positions

```bash
curl https://sleping-apex.hf.space/api/v1/grid/2025/Bahrain
```

### Get Driver's Best Lap

```bash
# Get all laps for driver
curl "https://sleping-apex.hf.space/api/v1/laps/2025/Bahrain/VER?session_type=R"

# Get fastest lap overall
curl "https://sleping-apex.hf.space/api/v1/laps/2025/Bahrain/fastest?session_type=R"

# Get personal best laps
curl "https://sleping-apex.hf.space/api/v1/laps/2025/Bahrain/personal-best?session_type=R"
```

### Get Laps with Filtering

```bash
# Quick laps only
curl "https://sleping-apex.hf.space/api/v1/laps/2025/Bahrain?session_type=R&quicklaps=true"

# Laps on soft tyres
curl "https://sleping-apex.hf.space/api/v1/laps/2025/Bahrain?session_type=R&compound=SOFT"

# Exclude pit stops
curl "https://sleping-apex.hf.space/api/v1/laps/2025/Bahrain?session_type=R&exclude_pits=true"
```

### Get Telemetry for Analysis

```bash
# Full race telemetry
curl "https://sleping-apex.hf.space/api/v1/telemetry/2025/Bahrain/VER?session_type=R"

# Specific lap
curl "https://sleping-apex.hf.space/api/v1/telemetry/2025/Bahrain/VER?session_type=R&lap=10"

# DRS data only
curl "https://sleping-apex.hf.space/api/v1/telemetry/2025/Bahrain/VER/drs?session_type=R"

# Speed data only
curl "https://sleping-apex.hf.space/api/v1/telemetry/2025/Bahrain/VER/speed?session_type=R"
```

### Get Weather Data

```bash
# All weather data
curl "https://sleping-apex.hf.space/api/v1/weather/2025/Bahrain/R"

# Weather summary
curl "https://sleping-apex.hf.space/api/v1/weather/2025/Bahrain/R/summary"
```

### Get Track Status

```bash
# All track status
curl "https://sleping-apex.hf.space/api/v1/track-status/2025/Bahrain/R"

# Safety car periods
curl "https://sleping-apex.hf.space/api/v1/track-status/2025/Bahrain/R/safety-car"

# VSC periods
curl "https://sleping-apex.hf.space/api/v1/track-status/2025/Bahrain/R/vsc"
```

### Get Position Data

```bash
# All positions
curl "https://sleping-apex.hf.space/api/v1/positions/2025/Bahrain/R"

# Position changes
curl "https://sleping-apex.hf.space/api/v1/positions/2025/Bahrain/R/changes"

# Overtakes
curl "https://sleping-apex.hf.space/api/v1/positions/2025/Bahrain/R/overtakes"
```

### Get Pit Stops

```bash
# All pit stops
curl "https://sleping-apex.hf.space/api/v1/pit-stops/2025/Bahrain/R"

# With duration
curl "https://sleping-apex.hf.space/api/v1/pit-stops/2025/Bahrain/R?include_duration=true"

# Fastest pit stop
curl "https://sleping-apex.hf.space/api/v1/pit-stops/2025/Bahrain/R/fastest"

# Pit stop strategy
curl "https://sleping-apex.hf.space/api/v1/pit-stops/2025/Bahrain/R/strategy"
```

### Get Circuit Information

```bash
# Circuit info
curl "https://sleping-apex.hf.space/api/v1/circuits/2025/Bahrain"

# DRS zones
curl "https://sleping-apex.hf.space/api/v1/circuits/2025/Bahrain/drs-zones"

# Corners
curl "https://sleping-apex.hf.space/api/v1/circuits/2025/Bahrain/corners"
```

### Get Race Control Messages

```bash
# All messages
curl "https://sleping-apex.hf.space/api/v1/race-control/2025/Bahrain/R"

# Penalties only
curl "https://sleping-apex.hf.space/api/v1/race-control/2025/Bahrain/R/penalties"

# Investigations
curl "https://sleping-apex.hf.space/api/v1/race-control/2025/Bahrain/R/investigations"
```

### Get Sector Times

```bash
# All sectors
curl "https://sleping-apex.hf.space/api/v1/sectors/2025/Bahrain/R"

# Fastest sector 1
curl "https://sleping-apex.hf.space/api/v1/sectors/2025/Bahrain/fastest/sector1?session_type=R"

# Driver sectors
curl "https://sleping-apex.hf.space/api/v1/sectors/2025/Bahrain/R/VER"
```

### Get Gaps

```bash
# Gaps to leader
curl "https://sleping-apex.hf.space/api/v1/gaps/2025/Bahrain/R"

# Driver gaps
curl "https://sleping-apex.hf.space/api/v1/gaps/2025/Bahrain/R/VER"

# Gap to driver ahead
curl "https://sleping-apex.hf.space/api/v1/gaps/2025/Bahrain/R/VER/ahead"
```

### Get Tyre Data

```bash
# Tyre compounds
curl "https://sleping-apex.hf.space/api/v1/tyres/2025/Bahrain/R/compounds"

# Tyre strategy
curl "https://sleping-apex.hf.space/api/v1/tyres/2025/Bahrain/R/strategy"

# Driver stints
curl "https://sleping-apex.hf.space/api/v1/tyres/2025/Bahrain/R/VER/stints"
```

### Get Teams

```bash
# All teams
curl "https://sleping-apex.hf.space/api/v1/teams/2025"

# Team results (may take 30-60 seconds)
curl "https://sleping-apex.hf.space/api/v1/teams/2025/McLaren/results"
```

### Get Standings

```bash
# Driver standings (may take 30-60 seconds)
curl "https://sleping-apex.hf.space/api/v1/standings/2025/drivers"

# Constructor standings (may take 30-60 seconds)
curl "https://sleping-apex.hf.space/api/v1/standings/2025/constructors"

# Standings after specific event
curl "https://sleping-apex.hf.space/api/v1/standings/2025/drivers/after/Bahrain"
```

---

## Notes

- **Date Format:** All dates are in ISO 8601 format (e.g., `2025-04-13T15:00:00`)
- **Time Format:** Lap times use ISO 8601 duration format (e.g., `PT1M35S` = 1 minute 35 seconds)
- **Event Names:** Use partial names (e.g., "Bahrain" matches "Bahrain Grand Prix")
- **Driver Identifiers:** Use abbreviation (e.g., `VER`) or driver number (e.g., `1`)
- **Session Types:** `FP1`, `FP2`, `FP3`, `Q`, `R`, `S`, `SQ`
- **Caching:** First request may be slower as data is downloaded and cached
- **Rate Limiting:** No rate limits currently, but be respectful
- **Performance:** Some endpoints (standings, team results) may take 30-60 seconds as they process all events for a year
- **404 Responses:** A `404` doesn't always mean an error - it may indicate data isn't available for that session (e.g., no weather data, no pit stops)

---

## Interactive Documentation

Visit `/docs` for interactive Swagger UI documentation with all endpoints:
```
https://sleping-apex.hf.space/docs
```

---

## Support

For issues or questions, check the repository or API documentation at `/docs`.
