# Missing FastF1 Features Analysis

Based on the [FastF1 documentation](https://docs.fastf1.dev/examples/basics.html) and API reference, here are features we haven't mapped yet:

## 🔴 Missing Features

### 1. **Weather Data**
- **FastF1 Method:** `session.weather`
- **Description:** Weather conditions during the session (air temp, track temp, humidity, wind speed, etc.)
- **Suggested Endpoint:** 
  - `GET /api/v1/weather/{year}/{event_name}/{session_type}`
- **Data Available:** Air temperature, track temperature, humidity, wind speed, wind direction, pressure

### 2. **Track Status Data**
- **FastF1 Method:** `session.track_status_data`
- **Description:** Track status flags (green, yellow, red, safety car, VSC, etc.) with timestamps
- **Suggested Endpoint:**
  - `GET /api/v1/track-status/{year}/{event_name}/{session_type}`
- **Data Available:** Status changes, flag types, timestamps, status messages

### 3. **Position Data**
- **FastF1 Method:** `session.position_data`
- **Description:** Real-time position data for all drivers throughout the session
- **Suggested Endpoint:**
  - `GET /api/v1/positions/{year}/{event_name}/{session_type}`
  - `GET /api/v1/positions/{year}/{event_name}/{session_type}/{driver}`
- **Data Available:** Position changes over time, position at specific times

### 4. **Pit Stops**
- **FastF1 Method:** Extract from `session.laps` (PitInTime, PitOutTime columns)
- **Description:** Pit stop information (when, duration, lap number)
- **Suggested Endpoint:**
  - `GET /api/v1/pit-stops/{year}/{event_name}/{session_type}`
  - `GET /api/v1/pit-stops/{year}/{event_name}/{session_type}/{driver}`
- **Data Available:** Pit stop times, durations, lap numbers, tyre changes

### 5. **Circuit/Track Information**
- **FastF1 Method:** `fastf1.get_circuit_info(year, event_name)`
- **Description:** Circuit layout, corner numbers, marshal sectors, track length
- **Suggested Endpoint:**
  - `GET /api/v1/circuits/{year}/{event_name}`
- **Data Available:** Track layout, corner numbers, marshal sectors, track length, coordinates

### 6. **Race Control Messages**
- **FastF1 Method:** `session.race_control_messages` (if available)
- **Description:** Race control announcements, penalties, investigations
- **Suggested Endpoint:**
  - `GET /api/v1/race-control/{year}/{event_name}/{session_type}`
- **Data Available:** Messages, timestamps, categories (penalties, investigations, etc.)

### 7. **Tyre Strategy Analysis**
- **FastF1 Method:** Analyze from `session.laps` (Compound, TyreLife, Stint columns)
- **Description:** Tyre strategy visualization and analysis
- **Suggested Endpoint:**
  - `GET /api/v1/tyre-strategy/{year}/{event_name}/{session_type}`
  - `GET /api/v1/tyre-strategy/{year}/{event_name}/{session_type}/{driver}`
- **Data Available:** Stint information, compound changes, tyre life

### 8. **Position Changes During Race**
- **FastF1 Method:** Analyze from `session.position_data` or `session.laps`
- **Description:** Position changes throughout the race
- **Suggested Endpoint:**
  - `GET /api/v1/position-changes/{year}/{event_name}/{session_type}`
  - `GET /api/v1/position-changes/{year}/{event_name}/{session_type}/{driver}`
- **Data Available:** Position at each lap, position changes, overtakes

### 9. **Sector Times Analysis**
- **FastF1 Method:** Extract from `session.laps` (Sector1Time, Sector2Time, Sector3Time)
- **Description:** Sector-by-sector analysis
- **Suggested Endpoint:**
  - `GET /api/v1/sectors/{year}/{event_name}/{session_type}`
  - `GET /api/v1/sectors/{year}/{event_name}/{session_type}/{driver}`
- **Data Available:** Sector times, fastest sectors, sector comparisons

### 10. **Session Status Information**
- **FastF1 Method:** `session.status` (if available)
- **Description:** Session start/finish status, session state
- **Note:** We partially have this but could expand it
- **Suggested Enhancement:** More detailed session status information

### 11. **Driver Standings (Championship)**
- **FastF1 Method:** Not directly in FastF1, but can be calculated from results
- **Description:** Championship standings after each race
- **Suggested Endpoint:**
  - `GET /api/v1/standings/{year}/drivers`
  - `GET /api/v1/standings/{year}/constructors`
  - `GET /api/v1/standings/{year}/after/{event_name}`

### 12. **Lap-by-Lap Position**
- **FastF1 Method:** Extract from `session.laps` (Position column)
- **Description:** Position of each driver at the end of each lap
- **Suggested Endpoint:**
  - `GET /api/v1/lap-positions/{year}/{event_name}/{session_type}`
  - `GET /api/v1/lap-positions/{year}/{event_name}/{session_type}/{driver}`

### 13. **Speed Traces**
- **FastF1 Method:** Extract from telemetry (Speed column)
- **Description:** Speed data along the track
- **Note:** We have this in telemetry, but could add a dedicated endpoint
- **Suggested Endpoint:**
  - `GET /api/v1/speed-traces/{year}/{event_name}/{driver}/{lap}`

### 14. **Gap to Leader**
- **FastF1 Method:** Calculate from position data or lap times
- **Description:** Time gaps to race leader
- **Suggested Endpoint:**
  - `GET /api/v1/gaps/{year}/{event_name}/{session_type}`
  - `GET /api/v1/gaps/{year}/{event_name}/{session_type}/{driver}`

## 📊 Summary

### Currently Implemented ✅
- Events & Sessions
- Results (Race, Qualifying, Sprint, Sprint Qualifying)
- Laps (all laps, driver-specific, fastest)
- Telemetry (full telemetry, car data)
- Drivers (list, event-specific)

### Missing but Available in FastF1 🔴
1. Weather data
2. Track status/flags
3. Position data (real-time positions)
4. Pit stops (dedicated endpoint)
5. Circuit information
6. Race control messages
7. Tyre strategy analysis
8. Position changes
9. Sector times analysis
10. Lap-by-lap positions
11. Gap to leader

### Partially Implemented ⚠️
- Session status (basic info only)
- Tyre data (included in laps but no dedicated strategy endpoint)
- Position data (included in laps but no real-time position endpoint)

## 🎯 Priority Recommendations

**High Priority:**
1. **Weather Data** - Very useful for race analysis
2. **Track Status** - Important for understanding race events
3. **Pit Stops** - Essential race data
4. **Circuit Information** - Useful for track visualization

**Medium Priority:**
5. **Position Data** - Real-time position tracking
6. **Tyre Strategy** - Strategy analysis
7. **Position Changes** - Overtake analysis

**Low Priority:**
8. **Race Control Messages** - Nice to have
9. **Sector Times** - Can be extracted from laps
10. **Gap to Leader** - Can be calculated

