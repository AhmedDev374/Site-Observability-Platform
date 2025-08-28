1. **Prometheus Targets:**  
![prometheus_targets](Images/grafanaa_packer_loss(high).PNG)

2. **Prometheus Alert:**  
![prometheus_alert](Images/prometheus_alert.PNG)

3. **Grafana DataSource:**  
![grafana_datasource](images/grafana_data_source.PNG)  

4. **Grafana Dashboard:**  
![grafana_dashboard](Images/grafanaa_packer_loss(high).PNG)

---

# Site-Observability-Platform

> A complete observability solution built with **Prometheus** and **Grafana**, designed to monitor site services, system health, and performance metrics in real-time.

---

## Table of Contents

- [Overview](#overview)  
- [Architecture](#architecture)  
- [Features](#features)  
- [Prerequisites](#prerequisites)  
- [Installation & Setup](#installation--setup)  
- [Usage](#usage)  
- [Configuration & Environment Variables](#configuration--environment-variables)  
- [Project Structure](#project-structure)  
- [Troubleshooting](#troubleshooting)  
- [Contact](#contact)  
- [License](#license)

---

## Overview

**Site-Observability-Platform** provides visibility into infrastructure and site services by combining:

1. **Prometheus** – Collects and stores metrics in a time-series database  
2. **Grafana** – Dashboards and visualization layer  
3. **Alertmanager** – Handles alerts and notifications  
4. **Custom Exporters** – Expose site-specific service metrics  

This platform helps track site uptime, performance, and service reliability with ready-to-use dashboards and alerts.

---

## Architecture

```plaintext
┌─────────────────┐     ┌─────────────┐     ┌─────────────────┐
│                 │     │             │     │                 │
│   Grafana UI    ◄─────┤ Prometheus  ├─────► Alertmanager    │
│                 │     │             │     │                 │
└─────────────────┘     └──────┬──────┘     └─────────────────┘
                               │
                     ┌─────────▼─────────┐
                     │                   │
                     │   Site Exporters  │
                     │                   │
                     └───────────────────┘
```
All services are containerized and orchestrated via Docker Compose for easy deployment and management.

---
## Feature

Ensure the following are installed on your system:
  - Real-time packet loss detection and monitoring
  - Network latency tracking and visualization
  - Pre-configured Grafana dashboards for immediate insights
  - Containerized deployment for easy setup and scalability

---

## Prerequisites

Ensure the following are installed on your system:

1. **Docker** – 24.x or later
2. **Docker Compose** – v2.x (included with recent Docker Desktop)

Verify:

```plaintext
docker --version
docker compose version
```

---

## Installation & Setup

1. **Clone the repository**:
```plaintext
git clone https://github.com/AhmedDev374/PrometheusFlow.git
cd PrometheusFlow
```

2. **Build and start the stack:**:
```plaintext
docker compose up --build
```
Then open .env and set your environment variables (DB credentials, ports, etc.).

3. **Access the services:**:

  - **Grafana** UI: ```http://localhost:3000```
  - **Prometheus**: ```http://localhost:9090```
  - **Alertmanager**: ```http://localhost:9093```
  - **Metrics KPI**: ```http://localhost:5001/metrics```
  - **PacketLoss On/Off**: ```http://localhost:5001/test/packetloss/on[off]```
  - **Latency On/Off**: ```http://localhost:5001/test/latency/on[off]```

---

## Usage
**Monitoring Network Performance**

1. Access the Grafana dashboard at http://localhost:3000
2. Navigate to the "Network Monitoring" dashboard
3. View real-time metrics for packet loss, latency, and network performance

**Configuring Alerts**

1. Modify alert rules in ```prometheus/alert.rules.yml```
2. Configure notification channels in ```alertmanager/alertmanager.yml```
3. Reload Prometheus configuration after changes:

```plaintext
docker compose exec prometheus kill -HUP 1
```
**Adding Custom Metrics**

1. Place custom exporters in the ```exporters/``` directory
2. Update ```prometheus/prometheus.yml``` to add new scrape target
3. Restart the Prometheus service:
```plaintext
docker compose restart prometheus
```
---

## Configuration & Environment Variables

**Environment Variables**
Create a ```.env``` file to customize the deployment:

```plaintext
# Grafana Configuration
GF_SECURITY_ADMIN_USER=admin
GF_SECURITY_ADMIN_PASSWORD=secure_password
GF_USERS_ALLOW_SIGN_UP=false

# Prometheus Configuration
PROMETHEUS_RETENTION=15d
PROMETHEUS_SCrape_INTERVAL=15s

# Alertmanager Configuration
ALERTMANAGER_SMTP_HOST=smtp.gmail.com
ALERTMANAGER_SMTP_PORT=587
ALERTMANAGER_SMTP_FROM=alerts@example.com
```
**Port Configuration**

Modify ```docker-compose.yml``` to change exposed ports if defaults are occupied.

---

## Project Structure
```plaintext
PrometheusPacketSentinel/
├── docker-compose.yml          # Main compose file
├── prometheus/
│   ├── prometheus.yml          # Main Prometheus configuration
│   └── alert.rules.yml         # Alerting rules
├── alertmanager/
│   └── alertmanager.yml        # Alertmanager configuration
├── grafana/
│   ├── provisioning/
│   │   ├── dashboards/         # Pre-configured dashboards
│   │   └── datasources/        # Data source configurations
│   └── config.ini              # Grafana configuration
├── exporters/
│   └── custom-exporter/        # Custom metric exporters
└── README.md                   # This documentation
```
---

## Troubleshooting

**Common Issues**
  1. **Port conflicts:** Change exposed ports in ```docker-compose.yml```
  2. **Permission issues:** Ensure Docker has proper permissions to create volumes
  3. **Container failures:** Check logs with ```docker compose logs [service_name]```
  4. Metrics not showing: Verify scrape configurations in ```prometheus/prometheus.yml```

**Logs Inspection**
```plaintext
# View logs for all services
docker compose logs

# View logs for specific service
docker compose logs prometheus
docker compose logs grafana
```

**Restart Services**
```plaintext
# Restart specific service
docker compose restart prometheus

# Rebuild and restart all services
docker compose up -d --build
```

---

## Contact

For questions or feedback, reach out to Ahmed at

1. **LinkDin**: https://eg.linkedin.com/in/ahmed-atef-elnadi-8165a51b9

---

## License

This project is licensed under the **GNU General Public License v3.0**.  
See the full license text here: [LICENSE](LICENSE).

