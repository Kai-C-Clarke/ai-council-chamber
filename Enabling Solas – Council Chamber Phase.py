# Enabling Solas – Council Chamber Phase One
# Flask-based AI Message Hub for Reflective Dialogue

from flask import Flask, request, render_template, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# Data file path
DATA_FILE = 'council_log.json'

# Ensure log exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f, indent=2)

# Load messages from JSON
def load_messages():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Save messages to JSON
def save_message(entry):
    messages = load_messages()
    messages.append(entry)
    with open(DATA_FILE, 'w') as f:
        json.dump(messages, f, indent=2)

@app.route('/')
def index():
    messages = load_messages()
    return render_template('index.html', messages=messages)

@app.route('/post', methods=['POST'])
def post():
    sender = request.form.get('from', 'Unknown')
    message = request.form.get('message', '')
    role = request.form.get('role', 'Unknown')
    timestamp = datetime.utcnow().isoformat()

    entry = {
        'from': sender,
        'role': role,
        'message': message,
        'timestamp': timestamp
    }

    save_message(entry)
    return jsonify(success=True)

@app.route('/messages', methods=['GET'])
def get_messages():
    return jsonify(load_messages())

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    sender = data.get('from', 'Unknown')
    message = data.get('message', '')
    role = data.get('role', 'AI')
    timestamp = datetime.utcnow().isoformat()

    entry = {
        'from': sender,
        'role': role,
        'message': message,
        'timestamp': timestamp
    }

    save_message(entry)
    return jsonify(success=True, status="Message received from webhook")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

