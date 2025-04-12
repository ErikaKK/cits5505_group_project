from app.main import bp
from flask import Flask, render_template
from flask_login import current_user


@bp.route("/account")
def account():
    return render_template(
        "/account/profile.html", title="My Account", login=current_user.is_authenticated
    )
