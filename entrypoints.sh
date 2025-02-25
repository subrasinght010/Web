#!/bin/bash

set -e

echo "Waiting for database..."
while ! nc -z db 5432; do   
  sleep 1
done
echo "Database is ready!"

echo "Starting Flask app with Gunicorn..."
exec gunicorn -w 4 -b 0.0.0.0:8000 app:app
