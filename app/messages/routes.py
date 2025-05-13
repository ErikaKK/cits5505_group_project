import json
from flask import jsonify, render_template, request
from flask_login import login_required, current_user
from app.models import Message, SpotifyData, User
from app.messages import bp
from app import db


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
                "sender_id": msg.sender_id,
                "receiver_id": msg.receiver_id,
                "sender": user_map.get(msg.sender_id, "Unknown"),
                "receiver": user_map.get(msg.receiver_id, "Unknown"),
                "message": msg.message,
                "created_at": msg.created_at,
                "shared_data": msg.shared_data,
                "is_self": msg.sender_id
                == msg.receiver_id,  # Add flag for self-messages
            }
            for msg in messages
        ],
    )


@bp.route("/messages/send", methods=["POST"])
@login_required
def send_message():
    receiver_id = request.form.get("receiver_id")
    message = request.form.get("message", "")
    shared_file = request.files.get("shared_file")

    if not receiver_id:
        return jsonify({"success": False, "error": "Missing receiver_id"}), 400

    shared_data = None

    # Handle shared data if file is uploaded
    if shared_file:
        try:
            shared_data = json.load(shared_file)

        except Exception as e:
            return (
                jsonify({"success": False, "error": f"Invalid JSON file: {str(e)}"}),
                400,
            )

    try:
        receiver_user = User.query.get(receiver_id)
        if not receiver_user:
            return jsonify({"success": False, "error": "Receiver not found"}), 404

        # Create the Message, linking to SharedData if available
        msg = Message(
            sender_id=current_user.id,
            receiver_id=receiver_user.id,
            message=message,
            shared_data=shared_data,
        )
        db.session.add(msg)
        db.session.commit()

        return (
            jsonify(
                {
                    "success": True,
                    "message_obj": {
                        "id": msg.id,
                        "sender_id": msg.sender_id,
                        "receiver_id": msg.receiver_id,
                        "sender": current_user.username,
                        "receiver": receiver_user.username,
                        "message": msg.message,
                        "created_at": msg.created_at,
                        "shared_data": shared_data,
                    },
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route("/messages/find_user", methods=["POST"])
@login_required
def find_user():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"success": False, "error": "Email is required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"success": False}), 404

    return (
        jsonify({"success": True, "user_id": user.id, "username": user.username}),
        200,
    )
