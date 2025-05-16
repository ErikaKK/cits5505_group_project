import pytest
from app import create_app, db
from app.models import User


@pytest.fixture(scope="session")
def app():
    app = create_app("testing")

    with app.app_context():
        db.create_all()
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="session")
def test_client(app):
    return app.test_client()
