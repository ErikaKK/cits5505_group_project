from flask import (
    json,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    jsonify,
    send_file,
)
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.account.forms import ProfileForm, PasswordForm
from app.account import bp
from app.models import SpotifyData, User
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from app.account.visualisation import Visualisation
from app.messages.utils import send_message_internal


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


@bp.route("/user-info", methods=["GET"])
@login_required
def get_user_info():
    return jsonify(
        {
            "user_id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
        }
    )


@bp.route("/upload")
@login_required
def upload():
    return render_template(
        "/account/upload.html", title="Upload", login=current_user.is_authenticated
    )


@bp.route("/upload-file", methods=["POST"])
@login_required
def upload_file():
    try:
        file = request.files.get("json_file")
        if not file:
            return jsonify({"error": "No file provided"}), 400

        try:
            new_data = json.load(file)
            if not isinstance(new_data, list):
                return jsonify({"error": "Invalid JSON format: must be an array"}), 400
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON file"}), 400

        # Get existing data for the user
        existing_record = SpotifyData.query.filter_by(user_id=current_user.id).first()

        if existing_record:
            # Convert both datasets to pandas DataFrames
            existing_df = pd.DataFrame(existing_record.data)
            new_df = pd.DataFrame(new_data)

            # Convert timestamps to datetime
            existing_df["timestamp"] = pd.to_datetime(existing_df["ts"])
            new_df["timestamp"] = pd.to_datetime(new_df["ts"])
            existing_timestamps = set(existing_df["ts"])
            new_timestamps = set(new_df["ts"])

            # Extract dates for comparison
            existing_df["date"] = existing_df["timestamp"].dt.date
            new_df["date"] = new_df["timestamp"].dt.date

            # Find overlapping dates
            overlapping_dates = set(existing_df["date"]).intersection(
                set(new_df["date"])
            )

            if overlapping_dates:
                # Check for real conflicts in overlapping dates
                real_conflicts = False
                overlapping_timestamps = existing_timestamps.intersection(
                    new_timestamps
                )

                if overlapping_timestamps:
                    # Check if the overlapping entries are identical

                    for ts in overlapping_timestamps:
                        existing_entry = existing_df[existing_df["ts"] == ts].iloc[0]
                        new_entry = new_df[new_df["ts"] == ts].iloc[0]

                        # Compare all fields except 'ts'
                        if not all(
                            existing_entry[col] == new_entry[col]
                            for col in existing_entry.index
                            if col != "ts"
                        ):
                            real_conflicts = True

                # Function to check for nearby timestamps
                def find_nearby_records(timestamp, df, window_minutes=1):
                    time_delta = pd.Timedelta(minutes=window_minutes)
                    mask = (df["timestamp"] >= timestamp - time_delta) & (
                        df["timestamp"] <= timestamp + time_delta
                    )
                    return df[mask]

                # Check for conflicts
                for _, new_row in new_df.iterrows():
                    nearby = find_nearby_records(new_row["timestamp"], existing_df)
                    if not nearby.empty:
                        real_conflicts = True

                if real_conflicts:
                    # Real conflicts found
                    return (
                        jsonify(
                            {
                                "status": "conflict",
                                "message": "Conflicting data found.",
                                "details": {
                                    "overlapping_dates": len(overlapping_dates)
                                },
                            }
                        ),
                        409,
                    )
                else:
                    # No real conflicts, merge all non-duplicate entries
                    existing_times = set(existing_df["ts"])
                    new_entries = [
                        entry for entry in new_data if entry["ts"] not in existing_times
                    ]

                    # Merge and sort
                    merged_data = existing_record.data + new_entries
                    merged_data.sort(key=lambda x: x["ts"])

                    existing_record.data = merged_data
                    db.session.commit()

                    return jsonify(
                        {
                            "success": True,
                            "message": "Data merged successfully",
                            "details": {
                                "new_entries_added": len(new_entries),
                            },
                        }
                    )
            else:
                # No overlapping dates, safe to merge all
                merged_data = existing_record.data + new_data
                merged_data.sort(key=lambda x: x["ts"])

                existing_record.data = merged_data
                db.session.commit()

                return jsonify(
                    {
                        "success": True,
                        "message": "Data merged successfully",
                        "details": {"new_entries_added": len(new_data)},
                    }
                )
        else:
            # First time upload
            new_data.sort(key=lambda x: x["ts"])
            new_record = SpotifyData(user_id=current_user.id, data=new_data)
            db.session.add(new_record)
            db.session.commit()

            return jsonify(
                {
                    "success": True,
                    "message": "Data uploaded successfully",
                    "details": {"entries_added": len(new_data)},
                }
            )

    except Exception as e:
        db.session.rollback()
        print(f"Upload error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@bp.route("/replace-data", methods=["POST"])
@login_required
def replace_data():
    try:
        new_data = request.get_json().get("new_data")
        if not new_data:
            return jsonify({"error": "No data provided"}), 400

        existing_record = SpotifyData.query.filter_by(user_id=current_user.id).first()
        if existing_record:
            existing_record.data = new_data
            db.session.commit()
            return jsonify({"success": True, "message": "Data replaced successfully"})
        else:
            return jsonify({"error": "No existing record found"}), 404

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@bp.route("/share-data", methods=["POST"])
@login_required
def share_data():
    try:
        data = request.get_json()
        receiver_email = data.get("receiverEmail")
        message = data.get("message")
        start_date = datetime.strptime(data.get("startDate"), "%Y-%m-%d")
        end_date = datetime.strptime(data.get("endDate"), "%Y-%m-%d")

        # Get user's data
        user_data = SpotifyData.query.filter_by(user_id=current_user.id).first()
        if not user_data:
            return jsonify({"error": "No data found"}), 404

        # Convert to DataFrame and filter by date range
        df = pd.DataFrame(user_data.data)
        df["timestamp"] = pd.to_datetime(df["ts"])
        filtered_df = df[
            (df["timestamp"].dt.date >= start_date.date())
            & (df["timestamp"].dt.date <= end_date.date())
        ]

        # Convert DataFrame to dict and ensure timestamps are strings
        filtered_data = []
        for record in filtered_df.to_dict("records"):
            # Convert any Timestamp objects to strings
            cleaned_record = {}
            for key, value in record.items():
                if isinstance(value, pd.Timestamp):
                    cleaned_record[key] = value.isoformat()
                else:
                    cleaned_record[key] = value
            filtered_data.append(cleaned_record)

        # Use your existing function to send the message
        try:
            send_message_internal(
                sender_id=current_user.id,
                receiver_email=receiver_email,
                message=message,
                shared_data=filtered_data,
            )
            return jsonify({"success": True, "message": "Data shared successfully"})
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "/account/dashboard.html",
        title="Dashboard",
        login=current_user.is_authenticated,
    )


@bp.route("/visualise/date-range", methods=["GET"])
@login_required
def get_date_range():
    try:
        # Get user's data from database
        user_data = SpotifyData.query.filter_by(user_id=current_user.id).first()
        if not user_data:
            return jsonify({"error": "No data found"}), 404

        # Convert stored JSON data to DataFrame
        df = pd.DataFrame(user_data.data)

        # Convert ts to datetime
        df["timestamp"] = pd.to_datetime(df["ts"])

        # Get min and max dates
        min_date = df["timestamp"].min().strftime("%Y-%m-%d")
        max_date = df["timestamp"].max().strftime("%Y-%m-%d")

        return jsonify(
            {
                "min_date": min_date,
                "max_date": max_date,
            }
        )

    except Exception as e:
        print(f"Error in get_date_range: {str(e)}")  # Add debug print
        return jsonify({"error": str(e)}), 500


@bp.route("/visualise/dashboard", methods=["POST"])
@login_required
def visualise_dashboard():
    try:
        # Get date range from request
        data = request.get_json()

        # Validate date inputs
        if not data or "startDate" not in data or "endDate" not in data:
            return jsonify({"error": "Start and end dates are required"}), 400

        if not data["startDate"] or not data["endDate"]:
            return jsonify({"error": "Start and end dates cannot be empty"}), 400

        try:
            start_date = datetime.strptime(data["startDate"], "%Y-%m-%d")
            end_date = datetime.strptime(data["endDate"], "%Y-%m-%d")
        except ValueError as e:
            return jsonify({"error": f"Invalid date format: {str(e)}"}), 400

        if start_date > end_date:
            return jsonify({"error": "Start date cannot be after end date"}), 400

        # Get user's data from database
        user_data = SpotifyData.query.filter_by(user_id=data["userId"]).first()
        if not user_data:
            return jsonify({"error": "No data found"}), 404

        # Convert stored JSON data to DataFrame
        df = pd.DataFrame(user_data.data)

        # Convert timestamp column
        df["timestamp"] = pd.to_datetime(df["ts"])

        # Filter by date range
        df = df[
            (df["timestamp"].dt.date >= start_date.date())
            & (df["timestamp"].dt.date <= end_date.date())
        ]

        if df.empty:
            return jsonify({"error": "No data found for selected date range"}), 404

        # Create Visualisation
        viz = Visualisation()

        # Process the filtered data
        viz.process_data(df)

        # Create a BytesIO object to store the image
        img_bytesio = BytesIO()

        # Create the Visualisation
        figure, axis = plt.subplots(2, 2, figsize=(14, 10), facecolor="white")
        axis = axis.flatten()

        # Generate charts
        viz.top_artists_chart(axis[0])
        viz.top_tracks_chart(axis[1])
        viz.monthly_time_spent(axis[2])
        viz.avg_daily_minutes_chart(axis[3])

        plt.tight_layout()

        # Add date range to the figure
        plt.figtext(
            0.5,
            0.02,
            f"Date Range: {start_date.date()} to {end_date.date()}",
            ha="center",
            fontsize=10,
        )

        # Save to BytesIO
        plt.savefig(img_bytesio, format="png", bbox_inches="tight", dpi=100)
        plt.close(figure)

        img_bytesio.seek(0)

        return send_file(img_bytesio, mimetype="image/png", as_attachment=False)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
