import os
import json
import requests
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()
OPENPROJECT_URL = os.getenv("OPENPROJECT_URL")
API_TOKEN = os.getenv("API_TOKEN")

# SMTP_SERVER = os.getenv("SMTP_SERVER")
# SMTP_PORT = int(os.getenv("SMTP_PORT"))
# SMTP_USER = os.getenv("SMTP_USER")
# SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# EMAIL_FROM = SMTP_USER
# EMAIL_TO = os.getenv("EMAIL_TO").split(",")

# --------------------------------------------------
# Project Configuration (ONLY THIS PROJECT)
# --------------------------------------------------
PROJECT_ALPHA1 = "106"   # ALPHA1 task list
# --------------------------------------------------
# Request headers
# --------------------------------------------------
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
# --------------------------------------------------
# Helper function to fetch counts
# --------------------------------------------------
def get_count(filters: list) -> int:
    url = f"{OPENPROJECT_URL}/api/v3/work_packages"
    response = requests.get(
        url,
        headers=HEADERS,
        params={"filters": json.dumps(filters)},
        auth=("apikey", API_TOKEN),
        timeout=30
    )
    response.raise_for_status()
    return response.json()["total"]

# --------------------------------------------------
# Filters (PROJECT-SCOPED)
# --------------------------------------------------

# Pending = Open + In Progress
pending_filter = [
    {"project": {"operator": "=", "values": [PROJECT_ALPHA1]}},
    {"status": {"operator": "=", "values": [1, 7]}}
]

# Closed
closed_filter = [
    {"project": {"operator": "=", "values": [PROJECT_ALPHA1]}},
    {"status": {"operator": "=", "values": [5]}}
]

# Bugs / Issues
bug_filter = [
    {"project": {"operator": "=", "values": [PROJECT_ALPHA1]}},
    {"type": {"operator": "=", "values": [1]}}
]

# # --------------------------------------------------
# # Fetch counts
# # --------------------------------------------------
# pending_count = get_count(pending_filter)
# closed_count = get_count(closed_filter)
# bug_count = get_count(bug_filter)


# print("✅ Daily ALPHA1 project report sent successfully.")
