import os
import time
import csv
import requests
import pandas as pd
from datetime import datetime, timedelta
from threading import Thread
from flask import Flask, send_file, jsonify
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import subprocess

# --- Config ---
SITES = {
    "Site1": "http://site1:5001/metrics",
    "Site2": "http://site2:5002/metrics",
    "Site3": "http://site3:5003/metrics",
    "Site4": "http://site4:5004/metrics",
    "Site5": "http://site5:5005/metrics",
}
EXPORT_DIR = "reports"
PDF_DIR = os.path.join(EXPORT_DIR, "pdf")
os.makedirs(PDF_DIR, exist_ok=True)

app = Flask(__name__)

# --- Utils ---
def parse_prometheus_metrics(text):
    metrics = {}
    for line in text.splitlines():
        if line.startswith("#"):
            continue
        if "{" in line:
            name, value = line.split(" ", 1)
            value = float(value)
            name = name.split("{")[0]
            metrics[name] = value
    return metrics

def save_to_csv(site, metrics):
    today = datetime.now().strftime("%Y-%m-%d")
    site_dir = os.path.join(EXPORT_DIR, site)
    os.makedirs(site_dir, exist_ok=True)
    file_path = os.path.join(site_dir, f"{today}.csv")

    file_exists = os.path.isfile(file_path)
    with open(file_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp"] + list(metrics.keys()))
        if not file_exists:
            writer.writeheader()
        row = {"timestamp": datetime.now().isoformat(), **metrics}
        writer.writerow(row)

def collect_and_store():
    for site, url in SITES.items():
        try:
            res = requests.get(url, timeout=5)
            metrics = parse_prometheus_metrics(res.text)
            save_to_csv(site, metrics)
            print(f"[OK] Stored metrics for {site}")
        except Exception as e:
            print(f"[ERR] {site}: {e}")

def background_collector():
    while True:
        collect_and_store()
        time.sleep(300)  # every 5 minutes

# --- Reporting ---
def generate_report(days=30):
    cutoff = datetime.now() - timedelta(days=days)
    all_data = []

    for site in SITES.keys():
        site_dir = os.path.join(EXPORT_DIR, site)
        if not os.path.isdir(site_dir):
            continue

        for file in os.listdir(site_dir):
            file_date = datetime.strptime(file.replace(".csv", ""), "%Y-%m-%d")
            if file_date >= cutoff:
                df = pd.read_csv(os.path.join(site_dir, file))
                df["site"] = site
                all_data.append(df)

    if all_data:
        final_df = pd.concat(all_data).sort_values(["site", "timestamp"])
        report_file = os.path.join(EXPORT_DIR, f"all_sites_last{days}days.csv")
        final_df.to_csv(report_file, index=False)
        generate_pdf_dashboard(final_df, days)  # Auto-generate PDF
        return report_file
    else:
        return None

# --- PDF Dashboard ---
def generate_pdf_dashboard(df, days):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    os.makedirs("temp_charts", exist_ok=True)

    charts = []

    # Example: average packet loss
    plt.figure(figsize=(6,4))
    sns.barplot(x='site', y='site_packet_loss_percent', data=df)
    plt.title("Average Packet Loss %")
    chart1 = "temp_charts/packet_loss.png"
    plt.savefig(chart1)
    plt.close()
    charts.append(("Packet Loss % by Site", chart1))

    # Example: average latency
    plt.figure(figsize=(6,4))
    sns.barplot(x='site', y='site_latency_ms', data=df)
    plt.title("Average Latency (ms)")
    chart2 = "temp_charts/latency.png"
    plt.savefig(chart2)
    plt.close()
    charts.append(("Latency (ms) by Site", chart2))

    # Create PDF
    pdf_file = os.path.join(PDF_DIR, f"dashboard_last{days}days.pdf")
    doc = SimpleDocTemplate(pdf_file, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(f"Network Metrics Dashboard - Last {days} Days", styles['Title']))
    elements.append(Spacer(1, 12))

    for title, chart_path in charts:
        elements.append(Paragraph(title, styles['Heading2']))
        elements.append(Image(chart_path, width=400, height=300))
        elements.append(Spacer(1, 12))

    # Summary table
    summary = df.groupby('site').mean().reset_index()
    data = [summary.columns.tolist()] + summary.round(2).values.tolist()
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.grey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    elements.append(Paragraph("Average Metrics per Site", styles['Heading2']))
    elements.append(table)

    doc.build(elements)
    print(f"[DONE] PDF Dashboard saved: {pdf_file}")

# --- Flask API ---
@app.route("/report/<int:days>", methods=["GET"])
def report(days):
    report_file = generate_report(days)
    if report_file:
        return send_file(report_file, as_attachment=True)
    else:
        return jsonify({"error": "No data available"}), 404

# --- Main ---
if __name__ == "__main__":
    # Start background collector
    t = Thread(target=background_collector, daemon=True)
    t.start()

    # Start Flask server
    app.run(host="0.0.0.0", port=5006)
