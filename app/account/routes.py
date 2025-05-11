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
from app.models import SharedData, User
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from app.account.visualisation import Visualisation


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


@bp.route("/upload")
@login_required
def upload():
    return render_template(
        "/account/upload.html", title="Upload", login=current_user.is_authenticated
    )


@bp.route("/shared_data/upload", methods=["POST"])
@login_required
def upload_shared_data():
    uploaded_file = request.files.get("json_file")
    if not uploaded_file:
        return jsonify({"success": False, "error": "No file uploaded."}), 400

    try:
        data = json.load(uploaded_file)
    except Exception as e:
        return jsonify({"success": False, "error": f"Invalid JSON: {str(e)}"}), 400

    try:
        # Save to SharedData table
        shared_data_obj = SharedData(user_id=current_user.id, data=data)
        db.session.add(shared_data_obj)
        db.session.commit()

        return jsonify({"success": True, "shared_data_id": shared_data_obj.id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


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
        user_data = SharedData.query.filter_by(user_id=current_user.id).first()
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
        user_data = SharedData.query.filter_by(user_id=current_user.id).first()
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

        # Create visualization
        viz = Visualisation()

        # Process the filtered data
        viz.process_data(df)

        # Create a BytesIO object to store the image
        img_bytesio = BytesIO()

        # Create the visualization
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
        print(f"Error in dashboard route: {str(e)}")
        return jsonify({"error": str(e)}), 500
