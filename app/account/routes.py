from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request,
    jsonify,
    current_app,
    send_file,
)
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.account.forms import ProfileForm, PasswordForm
from app.account import bp
from app.models import User
from app.account.visualisation import Visualisation
import tempfile
import json
import os
import pandas as pd
import matplotlib.pyplot as pyplot
from io import BytesIO


@bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    form = ProfileForm()

    # Pre-fill form data
    if request.method == "GET":
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email

    if form.validate_on_submit():
        try:
            print(form.username.data, current_user.username)
            print(form.first_name.data, current_user.first_name)
            print(form.last_name.data, current_user.last_name)
            print(form.email.data, current_user.email)
            if (
                form.username.data == current_user.username
                and (form.first_name.data or "").strip()
                == (current_user.first_name or "").strip()
                and (form.last_name.data or "").strip()
                == (current_user.last_name or "").strip()
                and form.email.data == current_user.email
            ):
                flash("Nothing has been changed!", "danger")
                return redirect(url_for("account.profile"))
            else:
                if form.first_name.data:
                    current_user.first_name = form.first_name.data
                if form.last_name.data:
                    current_user.last_name = form.last_name.data
                if form.username.data != current_user.username:
                    existing_username = User.query.filter(
                        (User.username == form.username.data)
                    ).first()
                    if existing_username:
                        flash(
                            "Username already exists. Please choose a different one.",
                            "danger",
                        )
                        return redirect(url_for("account.profile"))
                    current_user.username = form.username.data
                if form.email.data != current_user.email:
                    existing_email = User.query.filter(
                        User.email == form.email.data
                    ).first()
                    if existing_email:
                        flash(
                            "Email already exists. Please choose a different one.",
                            "danger",
                        )
                        return redirect(url_for("account.profile"))
                    current_user.email = form.email.data
            db.session.commit()
            flash("Profile updated successfully!", "success")
            return redirect(url_for("account.profile"))

        except Exception as e:
            db.session.rollback()
            flash(
                "An error occurred while updating your profile. Please try again.",
                "error",
            )

    return render_template(
        "account/profile.html",
        title="Profile",
        login=current_user.is_authenticated,
        form=form,
    )


@bp.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    password_form = PasswordForm()
    if password_form.validate_on_submit():
        if check_password_hash(
            current_user.password_hash, password_form.current_password.data
        ):
            current_user.password_hash = generate_password_hash(
                password_form.new_password.data
            )
            db.session.commit()
            flash("Password updated!", "success")

        else:
            flash("Current password is incorrect!", "danger")

    return render_template(
        "account/change-password.html",
        title="Change Password",
        login=current_user.is_authenticated,
        form=password_form,
    )


from functools import wraps
from werkzeug.serving import is_running_from_reloader
import signal


def timeout_decorator(seconds):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            def handler(signum, frame):
                raise TimeoutError(f"Request timed out after {seconds} seconds")

            # Set the timeout only if not in debug/reloader mode
            if not is_running_from_reloader():
                # Save the previous signal handler
                original_handler = signal.signal(signal.SIGALRM, handler)
                # Set the alarm
                signal.alarm(seconds)

            try:
                result = func(*args, **kwargs)
            finally:
                if not is_running_from_reloader():
                    # Disable the alarm
                    signal.alarm(0)
                    # Restore the previous signal handler
                    signal.signal(signal.SIGALRM, original_handler)

            return result

        return wrapper

    return decorator


@bp.route("/dashboard", methods=["GET", "POST"])
@timeout_decorator(300)
def dashboard():
    if request.method == "GET":
        return render_template("/account/dashboard.html")
    elif request.method == "POST":
        try:
            # Get JSON data directly from request
            data = request.get_json()

            # Create visualization
            viz = Visualisation()

            # Create a BytesIO object to store the image
            img_bytesio = BytesIO()

            # Process data directly without saving to file
            table = pd.DataFrame(data)
            table = table[
                [
                    "ts",
                    "ms_played",
                    "master_metadata_track_name",
                    "master_metadata_album_artist_name",
                ]
            ]
            table = table.rename(
                columns={
                    "ts": "timestamp",
                    "master_metadata_track_name": "track_name",
                    "master_metadata_album_artist_name": "artist_name",
                }
            )
            table["timestamp"] = pd.to_datetime(table["timestamp"])
            table["mins_played"] = table["ms_played"].apply(
                lambda x: round(x / 60000, 4)
            )
            table["hours_played"] = table["ms_played"].apply(
                lambda x: round(x / 3600000, 4)
            )
            table["time"] = table["timestamp"].dt.time
            table["hour"] = table["timestamp"].dt.hour

            # Create the visualization
            figure, axis = pyplot.subplots(2, 2, figsize=(14, 10), facecolor="white")
            axis = axis.flatten()

            # Set table attribute for visualization methods
            viz.table = table

            # Generate charts
            viz.top_artists_chart(axis[0])
            viz.top_tracks_chart(axis[1])
            viz.monthly_time_spent(axis[2])
            viz.avg_daily_minutes_chart(axis[3])

            pyplot.tight_layout()

            # Save to BytesIO instead of file
            pyplot.savefig(img_bytesio, format="png", bbox_inches="tight")
            pyplot.close(figure)  # Close the figure to free memory

            # Seek to start of BytesIO object
            img_bytesio.seek(0)

            # Return the image directly from memory
            return send_file(img_bytesio, mimetype="image/png", as_attachment=False)

        except Exception as e:
            print(f"Error in dashboard route: {e}")
            return jsonify({"error": str(e)}), 500
