from flask import Flask, jsonify
import requests

app = Flask(__name__)

ANOMALY_URL = "http://anomaly-service:5000/check"

@app.route("/optimize")
def optimize():
    try:
        result = requests.get(ANOMALY_URL).json()
        suggestion = "No action needed"
        
        if result["status"] == "Anomaly":
            if "latency" in result["message"].lower():
                suggestion = "Scale up network resources"
            elif "packet loss" in result["message"].lower():
                suggestion = "Check faulty nodes / reroute traffic"
        
        return jsonify({
            "network_status": result["status"],
            "issue": result["message"],
            "suggestion": suggestion
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
