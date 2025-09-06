#!/usr/bin/env python3
"""
Autor: Alvarado Becerra Ludwig - Ludway - theludway@gmail.com
CoAutor (Asistente de IA): ChatGPT - OpenAI
"""
import os
import time
import sys
import osmnx as ox
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def read_secret(path):
    """Read password from Docker secret"""
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def wait_for_db(engine, max_retries=30, delay=5):
    """Wait for database to be ready"""
    for attempt in range(max_retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Database connection successful!")
            return True
        except OperationalError as e:
            logger.warning(f"Database connection attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                logger.error("Max retries reached. Database is not available.")
                return False
    return False

def main():
    # Database configuration
    db_user = os.getenv("POSTGRES_USER", "admin")
    db_name = os.getenv("POSTGRES_DB", "osmdata")
    db_host = os.getenv("POSTGRES_HOST", "sotmlat2025_db")  # Use service name
    db_port = os.getenv("POSTGRES_PORT", "5432")
    db_password = os.getenv("POSTGRES_PASSWORD", "changeme")

    logger.info(f"Connecting to database: {db_user}@{db_host}:{db_port}/{db_name}")

    # Create database URL
    db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    try:
        # Create engine
        engine = create_engine(db_url, pool_pre_ping=True, pool_recycle=300)

        # Wait for database
        if not wait_for_db(engine):
            logger.error("Failed to connect to database. Exiting.")
            sys.exit(1)

        logger.info("Loading Medellín polygon from OpenStreetMap...")

        # Load Medellín polygon
        polygon = ox.geocode_to_gdf("Medellín, Colombia")

        logger.info("Saving polygon to PostGIS...")

        # Save to PostGIS
        polygon.to_postgis("city_boundary", engine, if_exists="replace", index=True)

        logger.info("Medellín polygon successfully loaded into PostGIS!")

        # Verify the data was inserted
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM city_boundary")).fetchone()
            logger.info(f"Inserted {result[0]} records into city_boundary table")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
