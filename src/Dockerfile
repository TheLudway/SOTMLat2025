# src/Dockerfile
FROM python:3.13-slim

# Install system dependencies for geopandas, osmnx, psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libgeos-dev \
    libproj-dev \
    libspatialindex-dev \
    && rm -rf /var/lib/apt/lists/*

# Create workdir
WORKDIR /app

# Copy requirements
COPY requirements.txt /app/

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . /app

# Run script
CMD ["python", "main.py"]
