#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "🚀 Running Render Build commands..."

# Run migrations
echo "🗄️ Running Django Database Migrations..."
python manage.py migrate

# Collect static files
echo "🎨 Collecting Static Files using WhiteNoise..."
python manage.py collectstatic --no-input

echo "✅ Render Build Completed Successfully!"
