import unittest
from app import create_app, db
from app.models import User, Message
from config import TestConfig
from datetime import datetime
import json


class TestMessages(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        # Create test users
        self.user1 = User(username="user1", email="user1@test.com")
        self.user1.set_password("password123")
        self.user2 = User(username="user2", email="user2@test.com")
        self.user2.set_password("password123")
        db.session.add_all([self.user1, self.user2])
        db.session.commit()

    def tearDown(self):
        """Clean up test environment"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, email, password):
        """Helper function to log in"""
        return self.client.post(
            "/auth/login",
            data={"email": email, "password": password},
            follow_redirects=True,
        )

    def test_send_message(self):
        """Test sending a message"""
        # Login as user1
        self.login("user1@test.com", "password123")

        # Send message
        response = self.client.post(
            "/messages/send",
            data={"receiver_id": self.user2.id, "message": "Test message"},
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data["success"])

        # Check message in database
        message = Message.query.first()
        self.assertEqual(message.sender_id, self.user1.id)
        self.assertEqual(message.receiver_id, self.user2.id)
        self.assertEqual(message.message, "Test message")

    def test_view_messages(self):
        """Test viewing messages"""
        # Create some test messages
        message1 = Message(
            sender_id=self.user1.id, receiver_id=self.user2.id, message="Message 1"
        )
        message2 = Message(
            sender_id=self.user2.id, receiver_id=self.user1.id, message="Message 2"
        )
        db.session.add_all([message1, message2])
        db.session.commit()

        # Login and view messages
        self.login("user1@test.com", "password123")
        response = self.client.get("/messages")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Message 1", response.data)
        self.assertIn(b"Message 2", response.data)

    def test_find_user(self):
        """Test finding user by email"""
        self.login("user1@test.com", "password123")

        response = self.client.post(
            "/messages/find_user", json={"email": "user2@test.com"}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertEqual(data["user_id"], self.user2.id)
