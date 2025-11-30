import time
import json
import logging
import threading
import os
import ast
from api.services.live_state import live_state

logger = logging.getLogger(__name__)

class LiveParser:
    def __init__(self, filename):
        self.filename = filename
        self.running = False
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._tail_and_parse)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)

    def _tail_and_parse(self):
        # Wait for file to exist
        start_time = time.time()
        while self.running and not os.path.exists(self.filename):
            if time.time() - start_time > 10:
                logger.error(f"Timeout waiting for live file: {self.filename}")
                return
            time.sleep(0.1)

        logger.info(f"Started parsing live file: {self.filename}")
        
        with open(self.filename, 'r') as f:
            # If we are attaching to an existing file, we might want to read from the beginning
            # to build the current state.
            while self.running:
                line = f.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                
                self._process_line(line)

    def _process_line(self, line):
        # Skip empty lines
        if not line.strip():
            return

        data = None
        try:
            # Try standard JSON first
            data = json.loads(line)
        except json.JSONDecodeError:
            try:
                # Try parsing as Python literal (handles single quotes)
                # FastF1 sometimes writes string representation of dicts
                data = ast.literal_eval(line)
            except (ValueError, SyntaxError):
                pass
        except Exception:
            pass

        if not data:
            return

        try:
            # Check for SignalR message structure
            if "M" in data and isinstance(data["M"], list):
                for msg in data["M"]:
                    # We are looking for the "feed" method
                    if msg.get("M") == "feed" and "A" in msg and isinstance(msg["A"], list):
                        args = msg["A"]
                        if len(args) >= 2:
                            category = args[0]
                            payload = args[1]
                            # timestamp = args[2] if len(args) > 2 else None
                            live_state.update(category, payload)
                            logger.info(f"Updated state for {category}") # Debug logging
        except Exception as e:
            logger.error(f"Error processing line: {e}")
            pass
