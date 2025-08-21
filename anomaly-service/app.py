from flask import Flask, jsonify
import requests

app = Flask(__name__)

MONITOR_URL = "http://monitor-service:5000/metrics"

@app.route("/check")
def check():
    try:
        data = requests.get(MONITOR_URL).json()
        anomaly = None
        
        if data["latency_ms"] > 150:
            anomaly = "High latency detected"
        elif data["packet_loss_percent"] > 3:
            anomaly = "High packet loss detected"
        
        return jsonify({
            "status": "Anomaly" if anomaly else "Normal",
            "message": anomaly or "All good",
            "metrics": data
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
