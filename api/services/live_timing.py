import threading
import os
import time
import logging
import json
from datetime import datetime
from fastf1.livetiming import SignalRClient
from api.services.live_parser import LiveParser
from api.services.live_state import live_state

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LiveTimingRecorder:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(LiveTimingRecorder, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.is_recording = False
        self.current_file = None
        self.start_time = None
        self.client = None
        self.thread = None
        self.parser = None
        self.output_dir = "live_data"
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def start_recording(self, filename: str = None):
        """Start recording live timing data."""
        with self._lock:
            if self.is_recording:
                return {"status": "error", "message": "Already recording"}

            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"live_timing_{timestamp}.json"
            
            if not filename.endswith('.json'):
                filename += '.json'
                
            self.current_file = os.path.join(self.output_dir, filename)
            
            # Reset state before new recording
            live_state.reset()
            
            # Create client
            try:
                # FastF1 SignalRClient writes to the specified file
                self.client = SignalRClient(filename=self.current_file, debug=True)
                
                # Run client in background thread
                self.thread = threading.Thread(target=self._run_client)
                self.thread.daemon = True
                self.thread.start()
                
                # Start parser to read the file and update state
                self.parser = LiveParser(self.current_file)
                self.parser.start()
                
                self.is_recording = True
                self.start_time = datetime.now()
                
                logger.info(f"Started recording live timing to {self.current_file}")
                return {
                    "status": "success", 
                    "message": "Recording started", 
                    "file": self.current_file
                }
            except Exception as e:
                logger.error(f"Failed to start recording: {e}")
                return {"status": "error", "message": str(e)}

    def _run_client(self):
        """Internal method to run the client."""
        try:
            if self.client:
                # This blocks until connection is closed
                self.client.start()
        except Exception as e:
            logger.error(f"Live timing client error: {e}")
        finally:
            self.is_recording = False
            logger.info("Live timing client stopped")

    def stop_recording(self):
        """Stop recording live timing data."""
        with self._lock:
            if not self.is_recording:
                return {"status": "error", "message": "Not recording"}
            
            # Stop parser
            if self.parser:
                self.parser.stop()
                self.parser = None
            
            # Note: We cannot easily stop the SignalRClient thread as it blocks on network.
            # It will eventually timeout or we can try to close it if we had access to the loop.
            # For now, we just mark as stopped.
            
            self.is_recording = False
            return {"status": "success", "message": "Recording marked as stopped"}

    def get_status(self):
        """Get current recording status."""
        return {
            "is_recording": self.is_recording,
            "current_file": self.current_file,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "duration": (datetime.now() - self.start_time).total_seconds() if self.is_recording and self.start_time else 0,
            "cars_tracked": len(live_state.cars)
        }

# Global instance
recorder = LiveTimingRecorder()
