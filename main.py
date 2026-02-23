import json
import os
import time
from daily_report import OpenProjectDailyReport
from mailer import send
from datetime import datetime
from timer import DailyTimer


STATUS_FILE = "last_status.json"


def load_previous_status():
    if not os.path.exists(STATUS_FILE):
        return None

    with open(STATUS_FILE, "r") as f:
        return json.load(f)


def save_current_status(status: dict):
    with open(STATUS_FILE, "w") as f:
        json.dump(status, f)


def job():
    report = OpenProjectDailyReport()
    current_status = report.get_project_status()

    previous_status = load_previous_status()

    if previous_status == current_status:
        print("No project status change found.")
        send({"message": "No project status change found."})
    else:
        print("Status changed. Sending full report.")
        send(current_status)
        save_current_status(current_status)


if __name__ == "__main__":
    timer = DailyTimer("config.json")
    print("Config loaded. Starting timer...")

    while True:     
        if timer.is_time_matched():
            job()
            print("Time matched. Generating report...")
            report = OpenProjectDailyReport()
            status = report.get_project_status()
            send(status)
            print("Pending :", status["pending_count"])
            print("Closed  :", status["closed_count"])
            print("Bugs    :", status["bug_count"])
        else:
            print("Time not matched.", datetime.now().strftime("%H:%M:%S"))
            time.sleep(timer.check_interval)

 