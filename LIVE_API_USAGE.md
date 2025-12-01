# Live Timing API Usage Guide

This guide explains how to use the Live Timing features of the FastF1 API to track Formula 1 sessions in real-time.

## Overview

The Live Timing API allows you to:
1.  **Connect** to the official F1 live data stream.
2.  **Record** the raw data to the server.
3.  **Parse** the data in real-time to get leaderboards, weather, and track status.
4.  **Consume** the parsed data via simple REST endpoints.

## Workflow

### 1. Start Recording

Before you can get any data, you must tell the server to start recording the live session.

**Endpoint:** `POST /api/v1/live/start`

**Example:**
```bash
curl -X POST "https://sleping-apex.hf.space/api/v1/live/start"
```

**Response:**
```json
{
  "data": {
    "status": "success",
    "message": "Recording started",
    "file": "live_data/live_timing_20251130_163721.json"
  },
  "meta": {
    "action": "start_recording"
  }
}
```

*Note: If a recording is already in progress, this will return an error. You can check the status first.*

### 2. Check Status

Verify that the recording is active and data is being tracked.

**Endpoint:** `GET /api/v1/live/status`

**Example:**
```bash
curl "https://sleping-apex.hf.space/api/v1/live/status"
```

**Response:**
```json
{
  "data": {
    "is_recording": true,
    "current_file": "live_data/live_timing_20251130_163721.json",
    "start_time": "2025-11-30T16:37:21.825839",
    "duration": 120.5,
    "cars_tracked": 20
  }
}
```

*   `is_recording`: Must be `true`.
*   `cars_tracked`: Should be > 0 if data is flowing.

### 3. Get Live Leaderboard

This is the main endpoint for building a live timing screen. It returns the current state of all drivers.

**Endpoint:** `GET /api/v1/live/leaderboard`

**Example:**
```bash
curl "https://sleping-apex.hf.space/api/v1/live/leaderboard"
```

**Response:**
```json
{
  "data": [
    {
      "driver_number": "1",
      "position": 1,
      "gap_to_leader": "0.0",
      "interval": "0.0",
      "last_lap_time": "1:32.450",
      "best_lap_time": "1:32.100",
      "sectors": {
        "1": {"Value": "29.969"},
        "2": {"Value": "41.200"},
        "3": {"Value": "21.281"}
      }
    },
    {
      "driver_number": "44",
      "position": 2,
      "gap_to_leader": "+2.500",
      "interval": "+2.500",
      ...
    }
  ],
  "meta": {
    "last_updated": "2025-11-30T16:40:00",
    "count": 20
  }
}
```

### 4. Get Live Weather

Track track temperature, air temperature, humidity, etc.

**Endpoint:** `GET /api/v1/live/weather`

**Example:**
```bash
curl "https://sleping-apex.hf.space/api/v1/live/weather"
```

### 5. Get Track Status

Check for Yellow Flags, Red Flags, Safety Car (SC), or Virtual Safety Car (VSC).

**Endpoint:** `GET /api/v1/live/track-status`

**Example:**
```bash
curl "https://sleping-apex.hf.space/api/v1/live/track-status"
```

### 6. Stop Recording

When the session is over, stop the recording to save resources.

**Endpoint:** `POST /api/v1/live/stop`

**Example:**
```bash
curl -X POST "https://sleping-apex.hf.space/api/v1/live/stop"
```

## Troubleshooting

*   **No Data / Empty Leaderboard:**
    *   Ensure a live F1 session is actually happening.
    *   Check `/live/log` to see if raw data is being written to the file.
    *   Wait 1-2 minutes after starting for the initial data sync.

*   **503 Service Unavailable:**
    *   The server might be restarting or deploying. Wait a few minutes.

*   **Recording won't start:**
    *   Check `/live/status`. If `is_recording` is true, you must stop it before starting a new one.
