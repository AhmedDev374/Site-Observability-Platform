# Use lightweight Python image
FROM python:3.10-slim

# Install dependencies
RUN pip install flask prometheus_client

# Work directory
WORKDIR /app

# By default run site1 (overridden with volume in docker-compose)
CMD ["python", "site4_simulator.py"]
