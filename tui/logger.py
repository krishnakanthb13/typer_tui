import json
import os
import time
from datetime import datetime

class Logger:
    def __init__(self, log_file="history.json"):
        # Ensure log file is in a valid location (e.g., user home or app dir)
        # For this CLI, we'll keep it local or in a consistent app dir
        self.log_file = log_file
        self.ensure_file()

    def ensure_file(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as f:
                json.dump([], f)

    def log_result(self, mode, duration, wpm, accuracy, raw_wpm):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "mode": mode,
            "duration": duration,
            "wpm": round(wpm, 2),
            "accuracy": round(accuracy, 2),
            "raw_wpm": round(raw_wpm, 2)
        }
        
        history = self.get_history()
        history.append(entry)
        
        with open(self.log_file, "w") as f:
            json.dump(history, f, indent=4)

    def get_history(self):
        try:
            with open(self.log_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
