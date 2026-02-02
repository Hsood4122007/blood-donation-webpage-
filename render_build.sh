#!/bin/sh
# Render build script for Blood Donation Platform

set -e  # Exit on any error

echo "Starting build process..."

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Build process completed successfully!"