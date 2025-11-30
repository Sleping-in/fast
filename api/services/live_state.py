import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class LiveRaceState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LiveRaceState, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.reset()

    def reset(self):
        self.cars = {}  # DriverNumber -> {Position, Gap, Interval, ...}
        self.weather = {}
        self.track_status = {}
        self.session_status = {}
        self.timing_data = {}
        self.lap_count = {}
        self.last_updated = datetime.now()

    def update(self, category, data):
        self.last_updated = datetime.now()
        logger.info(f"LiveState update: {category}")
        
        try:
            if category == "SessionStatus":
                self.session_status = data
            elif category == "TrackStatus":
                self.track_status = data
            elif category == "WeatherData":
                self.weather = data
            elif category == "TimingData":
                if "Lines" in data:
                    for driver_num, timing in data["Lines"].items():
                        if driver_num not in self.cars:
                            self.cars[driver_num] = {}
                        
                        # Update car data recursively or shallow merge
                        # F1 data sends partial updates
                        self._deep_update(self.cars[driver_num], timing)
                        
            elif category == "TimingAppData":
                if "Lines" in data:
                     for driver_num, app_data in data["Lines"].items():
                        if driver_num not in self.cars:
                            self.cars[driver_num] = {}
                        if "Stints" in app_data:
                            self.cars[driver_num]["Stints"] = app_data["Stints"]
                        if "Line" in app_data:
                             self.cars[driver_num]["Line"] = app_data["Line"] # Grid position etc
                             
            elif category == "LapCount":
                self.lap_count = data

        except Exception as e:
            logger.error(f"Error updating live state for {category}: {e}")

    def _deep_update(self, target, source):
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                self._deep_update(target[key], value)
            else:
                target[key] = value

    def get_leaderboard(self):
        leaderboard = []
        for driver_num, data in self.cars.items():
            entry = {"driver_number": driver_num}
            # Flatten some common fields for easier consumption
            if "Position" in data:
                entry["position"] = data["Position"]
            if "GapToLeader" in data:
                entry["gap_to_leader"] = data["GapToLeader"]
            if "IntervalToPositionAhead" in data:
                entry["interval"] = data["IntervalToPositionAhead"]
            if "BestLapTime" in data:
                entry["best_lap_time"] = data["BestLapTime"]
            if "LastLapTime" in data:
                entry["last_lap_time"] = data["LastLapTime"]
            if "Sectors" in data:
                entry["sectors"] = data["Sectors"]
            
            # Include raw data for completeness
            entry["raw"] = data
            leaderboard.append(entry)
        
        # Sort by position
        def get_pos(x):
            try:
                return int(x.get("position", 999))
            except:
                return 999
        
        leaderboard.sort(key=get_pos)
        return leaderboard

live_state = LiveRaceState()
