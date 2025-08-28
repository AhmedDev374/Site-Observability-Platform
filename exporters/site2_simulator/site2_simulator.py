from flask import Flask, Response
from prometheus_client import Gauge, generate_latest, CollectorRegistry
import random, time

app = Flask(__name__)
registry = CollectorRegistry()

SITE_NAME = "Site2"

# --- Core Metrics (existing) ---
packet_loss = Gauge("site_packet_loss_percent", "Packet loss percentage", ["site"], registry=registry)
latency = Gauge("site_latency_ms", "Network latency in ms", ["site"], registry=registry)
jitter = Gauge("site_jitter_ms", "Network jitter in ms", ["site"], registry=registry)
throughput = Gauge("site_throughput_mbps", "Network throughput in Mbps", ["site"], registry=registry)
availability = Gauge("site_availability_percent", "Availability in %", ["site"], registry=registry)
requests = Gauge("site_requests_total", "Number of requests/sessions", ["site"], registry=registry)
errors = Gauge("site_error_rate_percent", "Error rate percent", ["site"], registry=registry)
cpu = Gauge("site_cpu_usage_percent", "CPU usage %", ["site"], registry=registry)
memory = Gauge("site_memory_usage_percent", "Memory usage %", ["site"], registry=registry)
bandwidth = Gauge("site_bandwidth_utilization_percent", "Bandwidth utilization %", ["site"], registry=registry)

# --- Advanced Metrics ---
alarms = Gauge("site_alarms_count", "Number of active alarms", ["site"], registry=registry)
historical_events = Gauge("site_historical_events_count", "Number of historical events", ["site"], registry=registry)
call_setup_time = Gauge("site_call_setup_time_ms", "Call setup time in ms", ["site"], registry=registry)
dropped_sessions = Gauge("site_dropped_sessions_total", "Total dropped sessions", ["site"], registry=registry)
sla_compliance = Gauge("site_sla_compliance_percent", "Service SLA compliance %", ["site"], registry=registry)
geo_latitude = Gauge("site_geo_latitude", "Site latitude", ["site"], registry=registry)
geo_longitude = Gauge("site_geo_longitude", "Site longitude", ["site"], registry=registry)
anomaly_score = Gauge("site_anomaly_score", "Anomaly detection score", ["site"], registry=registry)
topology_links = Gauge("site_topology_links", "Number of links in network topology", ["site"], registry=registry)
predicted_traffic = Gauge("site_predicted_traffic_mbps", "Predicted traffic in Mbps", ["site"], registry=registry)

def update_metrics():
    """Randomly generate fake metrics for the site"""
    # Core metrics
    packet_loss.labels(SITE_NAME).set(random.uniform(0, 5))
    latency.labels(SITE_NAME).set(random.uniform(10, 200))
    jitter.labels(SITE_NAME).set(random.uniform(0, 50))
    throughput.labels(SITE_NAME).set(random.uniform(50, 1000))
    availability.labels(SITE_NAME).set(random.uniform(95, 100))
    requests.labels(SITE_NAME).set(random.randint(100, 1000))
    errors.labels(SITE_NAME).set(random.uniform(0, 5))
    cpu.labels(SITE_NAME).set(random.uniform(10, 90))
    memory.labels(SITE_NAME).set(random.uniform(10, 90))
    bandwidth.labels(SITE_NAME).set(random.uniform(10, 100))

    # Advanced metrics
    alarms.labels(SITE_NAME).set(random.randint(0, 10))
    historical_events.labels(SITE_NAME).set(random.randint(50, 500))
    call_setup_time.labels(SITE_NAME).set(random.uniform(100, 1000))
    dropped_sessions.labels(SITE_NAME).set(random.randint(0, 50))
    sla_compliance.labels(SITE_NAME).set(random.uniform(90, 100))

    # Fixed latitude and longitude
    geo_latitude.labels(SITE_NAME).set(29.9792)
    geo_longitude.labels(SITE_NAME).set(31.1342)

    anomaly_score.labels(SITE_NAME).set(random.uniform(0, 1))
    topology_links.labels(SITE_NAME).set(random.randint(1, 20))
    predicted_traffic.labels(SITE_NAME).set(random.uniform(50, 1200))

@app.route("/metrics")
def metrics():
    update_metrics()
    return Response(generate_latest(registry), mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
