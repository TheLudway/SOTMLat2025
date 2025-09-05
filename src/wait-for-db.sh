#!/bin/sh
set -e

host="$1"
shift
until pg_isready -h "$host" -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
  echo "Postgres is unavailable - sleeping"
  sleep 5
done

echo "Postgres is up - executing command"
exec "$@"
