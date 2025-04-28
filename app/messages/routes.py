import csv
import io
from flask import jsonify, render_template, request
from flask_login import login_required, current_user
from app.models import Message, User
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
                "created_at": msg.created_at,
                "shared_data": msg.shared_data,
            }
            for msg in messages
        ],
    )


@bp.route("/messages/send", methods=["POST"])
@login_required
def send_message():
    receiver_id = request.form.get("receiver_id")
    content = request.form.get("message")
    file = request.files.get("file")

    if not receiver_id:
        return jsonify({"success": False, "error": "Missing fields"}), 400

    if not content:
        content = "Hello, I want to share something with you!"

    shared_data = None
    if file:
        try:
            # Read file and parse CSV
            stream = io.StringIO(file.stream.read().decode("utf-8"))
            csv_reader = csv.reader(stream)
            shared_data = [row for row in csv_reader]
        except Exception as e:
            return (
                jsonify({"success": False, "error": f"Invalid CSV file: {str(e)}"}),
                400,
            )

    try:
        msg = Message(
            sender_id=current_user.id,
            receiver_id=int(receiver_id),
            message=content,
            shared_data=shared_data,
        )
        db.session.add(msg)
        db.session.commit()
        return jsonify({"success": True, "message": "Message sent!"}), 200
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
