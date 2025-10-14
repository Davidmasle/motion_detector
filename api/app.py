from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/status')
def status():
    log_path = 'logs/events.log'

    if not os.path.exists(log_path):
        return jsonify({"status": "no logs yet"})

    with open(log_path, 'r') as f:
        lines = f.readlines()

    if not lines:
        return jsonify({"status": "no events yet"})

    last_line = lines[-1].strip()
    return jsonify({"last_event": last_line})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
