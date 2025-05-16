import pytest
from app import create_app
from exts import db
from config import Config
from apps.front.models import FrontUser

# Pytest fixture to create a test client with an in-memory SQLite DB
@pytest.fixture
def client():
    app = create_app()
    app.config.update({
        'TESTING': True,                            # Enable testing mode
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',  # Use in-memory SQLite DB
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,    # Disable modification tracking
        'WTF_CSRF_ENABLED': False                   # Disable CSRF for test simplicity
    })

    with app.app_context():
        db.create_all()                             # Create all tables before test
        yield app.test_client()                     # Provide test client to test functions
        db.drop_all()                               # Drop all tables after test

# Test case: student login functionality
def test_student_login(client):
    with client.application.app_context():
        # Create a test user and add to the test DB
        user = FrontUser(username='Alice', email='alice@example.com', stu_id='11112222')
        user.password = 'Secret123'                 # Set password
        db.session.add(user)
        db.session.commit()

    # Simulate login form submission
    response = client.post('/signin/', data={
        'email': 'alice@example.com',
        'password': 'Secret123'
    }, follow_redirects=True)

    # ✅ Check JSON response
    assert response.status_code == 200              # Response should be OK
    json_data = response.get_json()                 # Parse JSON response
    assert json_data['code'] == 200                 # Expect success code
