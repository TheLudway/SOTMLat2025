#!/usr/bin/env python3
"""
Autor: Alvarado Becerra Ludwig - Ludway - theludway@gmail.com
CoAutor (Asistente de IA): ChatGPT - OpenAI
"""

import os
import osmnx as ox
from sqlalchemy import create_engine

# Read password from Docker secret
def read_secret(path):
    with open(path, "r") as f:
        return f.read().strip()

db_user = os.getenv("POSTGRES_USER", "admin")
db_name = os.getenv("POSTGRES_DB", "osmdata")
db_host = os.getenv("POSTGRES_HOST", "db")
db_port = os.getenv("POSTGRES_PORT", "5432")
db_password = os.getenv("POSTGRES_PASSWORD", "changeme")

db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(db_url)

# Load Medellín polygon
polygon = ox.geocode_to_gdf("Medellín, Colombia")
polygon.to_postgis("city_boundary", engine, if_exists="replace")

print("Medellín polygon loaded into PostGIS")
