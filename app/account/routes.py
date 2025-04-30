from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.account.forms import ProfileForm, PasswordForm
from app.account import bp
from app.models import User


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
            # Update user information
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
