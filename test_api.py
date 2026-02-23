import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("OPENPROJECT_URL")
API_TOKEN = os.getenv("API_TOKEN")

url = f"{BASE_URL}/api/v3/work_packages"

headers = {
    "Accept": "application/json"
}

r = requests.get(
    url,
    headers=headers,
    auth=("apikey", API_TOKEN)
)

print("STATUS:", r.status_code)
print("CONTENT-TYPE:", r.headers.get("Content-Type"))

print("TOTAL:", r.json()["total"])
