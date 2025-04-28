from app import db
from app.models import Message, User
from datetime import datetime


def send_message_internal(
    sender_id: int, receiver_email: str, message: str, shared_data=None
):
    if not sender_id or not receiver_email:
        raise ValueError("Sender ID and receiver email must both be provided.")

    # Find receiver user
    receiver_user = User.query.filter_by(email=receiver_email).first()
    if not receiver_user:
        raise ValueError(f"Receiver with email {receiver_email} not found.")

    # Create and commit in database
    msg = Message(
        sender_id=sender_id,
        receiver_id=receiver_user.id,
        message=message,
        shared_data=shared_data,
    )
    db.session.add(msg)
    db.session.commit()
