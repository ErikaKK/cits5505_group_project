from app.main import bp
from flask import Flask, render_template


@bp.route("/")
def index():
    return render_template("index.html", title="Home")
