from datetime import datetime
import json
import time


class DailyTimer:

    def __init__(self, config_path):
        self.config_path = config_path
        self.target_time = None
        self.check_interval = None
        self._last_trigger_date = None
        self.load_config()

    def load_config(self):
        with open(self.config_path, "r") as f:
            config = json.load(f)

        schedule = config["schedule"]
        self.target_time = schedule["target_time"]  # HH:MM:SS
        self.check_interval = schedule["check_interval_seconds"]

    def is_time_matched(self):

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        today = now.date()

        # Prevent multiple triggers same day
        if current_time == self.target_time and self._last_trigger_date != today:
            self._last_trigger_date = today
            return True

        return False

    def run(self, callback):

        print("⏳ Timer running...")
        print("🎯 Target time:", self.target_time)

        while True:
            now = datetime.now().strftime("%H:%M:%S")
            print("Checking time:", now)

            if self.is_time_matched():
                print("✅ Time matched. Running job...")
                callback()

            time.sleep(self.check_interval)