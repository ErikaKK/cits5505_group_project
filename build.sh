#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# Initialize migrations if they don't exist
# flask db init || true

# Create and run migrations
# flask db migrate
flask db upgrade
