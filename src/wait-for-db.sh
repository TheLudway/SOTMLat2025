#!/bin/sh
set -e

host="$1"
shift

echo "=== DEBUG INFO ==="
echo "Target host: $host"
echo "POSTGRES_USER: $POSTGRES_USER"
echo "POSTGRES_DB: $POSTGRES_DB"
echo "Current working directory: $(pwd)"
echo "Environment variables:"
env | grep -E "(POSTGRES|DB)" || echo "No POSTGRES/DB env vars found"

echo ""
echo "=== NETWORK DEBUG ==="
echo "Hostname resolution test:"
nslookup $host || echo "nslookup failed"
echo ""
echo "Ping test:"
ping -c 2 $host || echo "Ping failed"
echo ""
echo "Port connectivity test:"
nc -z -v $host 5432 || echo "Port 5432 not reachable"

echo ""
echo "=== WAITING FOR POSTGRESQL ==="
echo "Waiting for PostgreSQL at $host:5432..."

# Try multiple connection methods
until pg_isready -h "$host" -p 5432 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -t 10; do
  echo "Postgres is unavailable - sleeping for 5 seconds..."
  sleep 5
done

echo "PostgreSQL is ready!"

# Additional check - try to connect with psql
echo "Testing connection with psql..."
until PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$host" -p 5432 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT 1;" > /dev/null 2>&1; do
  echo "Connection test failed - sleeping for 5 seconds..."
  sleep 5
done

echo "Connection test successful! Executing command: $@"
exec "$@"
