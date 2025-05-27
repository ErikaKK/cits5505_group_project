from typing import Optional
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "user"
    __table_args__ = {"quote": True}

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    first_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(50))
    last_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(50))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User {}>".format(self.username)


class SpotifyData(db.Model):
    __tablename__ = "spotify-data"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    data = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        return f"<SpotifyData id={self.id}>"


class Message(db.Model):
    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.String, default=lambda: datetime.now(timezone.utc))
    shared_data = db.Column(db.JSON, nullable=True)

    def __repr__(self):
        return "<Message from {} to {} at {}: {}>".format(
            self.sender_id, self.receiver_id, self.created_at, self.message
        )
