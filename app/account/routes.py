from app.account import bp
from flask import Flask, render_template
from flask_login import current_user, login_required


@bp.route("/")
@bp.route("/profile")
@login_required
def profile():
    return render_template(
        "/account/profile.html", title="My Account", login=current_user.is_authenticated
    )
