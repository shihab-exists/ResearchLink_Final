#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
curl -sS https://api.aiven.io/v1/ca.pem -o ca.pem
python manage.py migrate
python manage.py collectstatic --no-input
