from flask import render_template
from flask_login import login_required, current_user
from app.models import Message
from app.messages import bp


# Render the messages for the logged-in user
@bp.route("/messages")
@login_required
def show_messages():
    messages = (
        Message.query.filter(
            (Message.sender_id == current_user.id)
            | (Message.receiver_id == current_user.id)
        )
        .order_by(Message.created_at.desc())
        .all()
    )
    return render_template("messages.html", messages=messages)
