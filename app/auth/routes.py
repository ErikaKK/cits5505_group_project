from app.auth import bp

from flask import render_template, redirect, url_for, flash

from app.auth.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index", login=current_user.is_authenticated))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password", "error")
            return redirect(url_for("auth.login", login=current_user.is_authenticated))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("main.index", login=current_user.is_authenticated))

    return render_template(
        "/auth/login.html",
        title="Sign In",
        form=form,
        login=current_user.is_authenticated,
    )


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index", login=current_user.is_authenticated))
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter(
            (User.username == form.username.data) | (User.email == form.email.data)
        ).first()
        if existing_user:
            flash(
                "Username or email already exists. Please choose a different one.",
                "danger",
            )
            return redirect(url_for("auth.login"))

        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You can now log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("/auth/register.html", title="Register", form=form)
