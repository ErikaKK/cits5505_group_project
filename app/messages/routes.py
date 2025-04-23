from flask import render_template
from flask_login import login_required, current_user
from app.models import Message, User
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

    # Preload user IDs to usernames
    user_ids = set(
        [msg.sender_id for msg in messages] + [msg.receiver_id for msg in messages]
    )
    users = User.query.filter(User.id.in_(user_ids)).all()
    user_map = {u.id: u.username for u in users}

    return render_template(
        "messages/messagelist.html",
        login=current_user.is_authenticated,
        messages=[
            {
                "id": msg.id,
                "sender": (
                    None
                    if msg.sender_id == current_user.id
                    else user_map.get(msg.sender_id, "Unknown")
                ),
                "receiver": (
                    None
                    if msg.receiver_id == current_user.id
                    else user_map.get(msg.receiver_id, "Unknown")
                ),
                "message": msg.message,
                "created_at": msg.created_at.isoformat() if msg.created_at else None,
                "shared_data": msg.shared_data,
            }
            for msg in messages
        ],
    )
