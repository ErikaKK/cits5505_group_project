#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Create/Update database
python << END
from app import app, db
from app.models import User  # Import your User model

with app.app_context():
    # Create all tables
    db.create_all()
    
    # Verify the tables exist
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print("Created tables:", tables)
END