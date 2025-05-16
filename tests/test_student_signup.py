import sys
import os
# ✅ Add the parent directory to sys.path to allow absolute imports
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
        'TESTING': True,                                # Enable testing mode
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',  # In-memory database for test
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,         # Disable modification tracking
        'WTF_CSRF_ENABLED': False                        # Disable CSRF protection in test
    })

    with app.app_context():
        db.create_all()                                 # Create tables before test
        yield app                                       # Provide app instance to test
        db.drop_all()                                   # Drop tables after test
        db.session.remove()                             # Clean up the session

# ✅ Create a client fixture for testing
@pytest.fixture
def client(test_app):
    return test_app.test_client()                       # Return test client from app

# ✅ Test registration functionality: send POST form to /signup/
def test_signup_success(client):
    response = client.post('/signup/', data={
        'email': 'alice@example.com',                   # Test email
        'username': 'Alice',                            # Test username
        'stu_id': '11112222',                           # Test student ID
        'password1': 'Secret123',                       # Password input
        'password2': 'Secret123'                        # Confirm password input
    }, follow_redirects=True)

    assert response.status_code == 200                  # Expect success response

    # ✅ Check if user is successfully registered in the database
    with client.application.app_context():
        user = FrontUser.query.filter_by(email='alice@example.com').first()
        assert user is not None                         # User should exist
        assert user.username == 'Alice'                 # Username should match
