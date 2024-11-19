#!/bin/bash

# Wait for the PostgreSQL service to be available
echo "Waiting for the database at $DB_HOST:$DB_PORT..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "Database is ready!"

# Run Django database migrations
echo "Running migrations..."
python cryptoapp/manage.py makemigrations --no-input
python cryptoapp/manage.py migrate --no-input

# Start the Django app
exec "$@"