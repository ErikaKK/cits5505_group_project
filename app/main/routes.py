from app.main import bp
from flask import Flask, render_template
from flask_login import current_user
from app.models import db


@bp.route("/")
def index():
    return render_template(
        "index.html", title="SpotifyDash", login=current_user.is_authenticated
    )


@bp.route("/debug-db")
def debug_db():
    try:
        # Try to create tables
        db.create_all()

        # Check what tables exist
        from sqlalchemy import inspect

        inspector = inspect(db.engine)
        tables = inspector.get_table_names()

        # Get database URI (will mask password)
        uri = str(db.engine.url)
        if "postgresql" in uri:
            uri = uri.split("@")[1]  # Only show host/database part

        return f"Database connected. URI: {uri}, Tables: {tables}"
    except Exception as e:
        return f"Database error: {str(e)}"
