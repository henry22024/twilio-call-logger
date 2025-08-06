from flask import Flask, request
import requests
import os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def log_call():
    data = request.form
    from_number = data.get("From")
    to_number = data.get("To")
    status = data.get("CallStatus")
    duration = data.get("CallDuration")
    recording_url = data.get("RecordingUrl")

    # Construct message
    body = f"""📞 Call Log:
From: {from_number}
To: {to_number}
Status: {status}
Duration: {duration or "N/A"} sec
🎧 Recording: {recording_url}.mp3"""

    # Send to Front
    front_payload = {
        "inbox_id": os.getenv("FRONT_INBOX_ID"),
        "body": body,
        "subject": "Twilio Call Recording",
        "author": {"type": "external", "handle": from_number}
    }

    headers = {
        "Authorization": f"Bearer {os.getenv('FRONT_API_TOKEN')}",
        "Content-Type": "application/json"
    }

    r = requests.post("https://api2.frontapp.com/conversations", json=front_payload, headers=headers)
    return "ok", 200
