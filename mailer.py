# mailer.py

import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

EMAIL_FROM = SMTP_USER
EMAIL_TO = os.getenv("EMAIL_TO").split(",")

def send(data: dict):

    # If only message present → short email
    if "message" in data:
        body = f"""
OpenProject Daily Summary

{data['message']}

-- Automated Report System
"""
    else:
        pending_count = data.get("pending_count", 0)
        closed_count = data.get("closed_count", 0)
        bug_count = data.get("bug_count", 0)

        body = f"""
OpenProject Daily Summary
📁 Project : ALPHA1 task list

📌 Pending Tasks : {pending_count}
✅ Closed Tasks  : {closed_count}
🐞 Bugs / Issues : {bug_count}

-- Automated Report System
"""

    msg = MIMEText(body)
    msg["Subject"] = "Daily OpenProject Task Summary – ALPHA1"
    msg["From"] = EMAIL_FROM
    msg["To"] = ", ".join(EMAIL_TO)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)

    print("📧 Email sent successfully.")