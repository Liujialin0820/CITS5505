import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app  # ✅ Unified import entry for the app package
from exts import db
from apps.front.models import FrontUser

# ✅ Create a test app instance, no arguments needed, configure manually
@pytest.fixture
def test_app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'WTF_CSRF_ENABLED': False
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
        db.session.remove()

# ✅ Create a client fixture for testing
@pytest.fixture
def client(test_app):
    return test_app.test_client()

# ✅ Test registration functionality: send POST form to /signup/
def test_signup_success(client):
    response = client.post('/signup/', data={
        'email': 'alice@example.com',
        'username': 'Alice',
        'stu_id': '11112222',
        'password1': 'Secret123',
        'password2': 'Secret123'
    }, follow_redirects=True)

    assert response.status_code == 200

    # ✅ Check if user is successfully registered in the database
    with client.application.app_context():
        user = FrontUser.query.filter_by(email='alice@example.com').first()
        assert user is not None
        assert user.username == 'Alice'
