from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

FRONT_INBOX_ID = os.getenv("FRONT_INBOX_ID")
FRONT_API_KEY = os.getenv("FRONT_API_KEY")

@app.route("/", methods=["POST"])
def receive_twilio_call():
    print("✅ Twilio Webhook triggered!")

    # Try to get data from both form and JSON
    try:
        data = request.form.to_dict() if request.form else request.get_json()
        print(f"📦 Raw incoming data: {data}")
    except Exception as e:
        print(f"❌ Error parsing incoming request: {str(e)}")
        return jsonify({"error": "Invalid request format"}), 400

    from_number = data.get("From")
    to_number = data.get("To")
    call_sid = data.get("CallSid")
    duration = data.get("CallDuration")
    recording_url = data.get("RecordingUrl")

    if not from_number or not call_sid:
        print("⚠️ Missing required fields. Skipping...")
        return jsonify({"error": "Missing required fields"}), 400

    # Format your Front note
    note = {
        "body": f"📞 New call received\nFrom: {from_number}\nTo: {to_number}\nDuration: {duration} sec\nSID: {call_sid}\nRecording: {recording_url or 'N/A'}",
        "external_id": call_sid,
        "target": {"type": "inbox", "id": FRONT_INBOX_ID}
    }

    print("➡️ Sending to Front API...")
    r = requests.post(
        "https://api2.frontapp.com/notes",
        headers={
            "Authorization": f"Bearer {FRONT_API_KEY}",
            "Content-Type": "application/json"
        },
        json=note
    )

    print(f"✅ Front API response: {r.status_code} | {r.text}")
    return jsonify({"status": "received"}), 200
