from flask import Flask, Response
import random, time

app = Flask(__name__)

simulate_latency = False
simulate_packet_loss = False

@app.route("/metrics")
def metrics():
    latency = random.uniform(10, 100)
    packet_loss = random.uniform(0, 2)
    throughput = random.uniform(50, 500)
    
    # Apply test simulation
    if simulate_latency:
        latency += 200
    if simulate_packet_loss:
        packet_loss += 5
    
    # Prometheus text format
    data = f"""
# HELP latency_ms Network latency in milliseconds
# TYPE latency_ms gauge
latency_ms {latency}

# HELP packet_loss_percent Packet loss in percentage
# TYPE packet_loss_percent gauge
packet_loss_percent {packet_loss}

# HELP throughput_mbps Network throughput in Mbps
# TYPE throughput_mbps gauge
throughput_mbps {throughput}
"""
    return Response(data, mimetype="text/plain")

# Test endpoints
@app.route("/test/latency/on")
def test_latency_on():
    global simulate_latency
    simulate_latency = True
    return "Latency simulation ON"

@app.route("/test/latency/off")
def test_latency_off():
    global simulate_latency
    simulate_latency = False
    return "Latency simulation OFF"

@app.route("/test/packetloss/on")
def test_packet_on():
    global simulate_packet_loss
    simulate_packet_loss = True
    return "Packet loss simulation ON"

@app.route("/test/packetloss/off")
def test_packet_off():
    global simulate_packet_loss
    simulate_packet_loss = False
    return "Packet loss simulation OFF"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
