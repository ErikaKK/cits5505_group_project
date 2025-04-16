from app.main import bp
from flask import Flask, render_template
from flask_login import current_user


@bp.route("/")
def index():
    return render_template(
        "index.html", title="Home", login=current_user.is_authenticated
    )
