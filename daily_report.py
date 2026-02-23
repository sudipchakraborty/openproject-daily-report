import os
import json
import requests
from dotenv import load_dotenv


class OpenProjectDailyReport:

    def __init__(self):
        load_dotenv()

        self.OPENPROJECT_URL = os.getenv("OPENPROJECT_URL")
        self.API_TOKEN = os.getenv("API_TOKEN")

        self.PROJECT_ALPHA1 = "106"

        self.HEADERS = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    # --------------------------------------------------
    # Helper function to fetch counts
    # --------------------------------------------------
    def get_count(self, filters: list) -> int:
        url = f"{self.OPENPROJECT_URL}/api/v3/work_packages"

        response = requests.get(
            url,
            headers=self.HEADERS,
            params={"filters": json.dumps(filters)},
            auth=("apikey", self.API_TOKEN),
            timeout=30
        )

        response.raise_for_status()
        return response.json()["total"]

    # --------------------------------------------------
    # Build filters
    # --------------------------------------------------
    def build_filters(self):

        pending_filter = [
            {"project": {"operator": "=", "values": [self.PROJECT_ALPHA1]}},
            {"status": {"operator": "=", "values": [1, 7]}}
        ]

        closed_filter = [
            {"project": {"operator": "=", "values": [self.PROJECT_ALPHA1]}},
            {"status": {"operator": "=", "values": [5]}}
        ]

        bug_filter = [
            {"project": {"operator": "=", "values": [self.PROJECT_ALPHA1]}},
            {"type": {"operator": "=", "values": [1]}}
        ]

        return pending_filter, closed_filter, bug_filter

    # --------------------------------------------------
    # Public method to get structured status
    # --------------------------------------------------
    def get_project_status(self) -> dict:

        pending_filter, closed_filter, bug_filter = self.build_filters()

        status = {
            "pending_count": self.get_count(pending_filter),
            "closed_count": self.get_count(closed_filter),
            "bug_count": self.get_count(bug_filter)
        }

        return status