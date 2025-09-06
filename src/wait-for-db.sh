#!/bin/sh
set -e

host="$1"
shift

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
