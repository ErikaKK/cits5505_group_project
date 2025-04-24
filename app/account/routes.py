from app.account import bp
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
import json


@bp.route("/")
@bp.route("/profile")
@login_required
def profile():
    return render_template(
        "/account/profile.html", title="My Account", login=current_user.is_authenticated
    )


@bp.route("/stats")
@login_required
def stats():
    return render_template(
        "/account/stats.html", title="My Account", login=current_user.is_authenticated
    )
