# Import application setup and models
from app import create_app
from exts import db
from config import Config
from apps.front.models import FrontUser
import pytest

# Pytest fixture to set up a test client with test database and session
@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True               # Enable testing mode
    app.config['WTF_CSRF_ENABLED'] = False     # Disable CSRF for tests

    # Setup test users inside application context
    with app.app_context():
        db.create_all()  # Create all tables

        # Insert test user 1 if not exists
        if not db.session.get(FrontUser, 1):
            db.session.add(FrontUser(
                id=1,
                email="user1@test.com",
                username="UserOne",
                password="testpass1",
                stu_id="12345678"
            ))

        # Insert test user 2 if not exists
        if not db.session.get(FrontUser, 2):
            db.session.add(FrontUser(
                id=2,
                email="user2@test.com",
                username="UserTwo",
                password="testpass2",
                stu_id="87654321"
            ))

        db.session.commit()

    # Create test client and simulate logged-in session
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess[Config.FRONT_USER_ID] = 1  # Simulate user 1 is logged in
        yield client  # Provide the client to test functions

# Test case: Send a message from user 1 to user 2 and verify it appears in chat history
def test_send_and_receive_message(client):
    # Prepare message payload
    payload = {
        'sender_id': 1,
        'receiver_id': 2,
        'content': 'Hello from unit test'
    }

    # Send POST request to simulate message sending
    res = client.post('/api/send_message', json=payload)
    print("🧪 POST STATUS:", res.status_code)
    assert res.status_code == 200  # Expect success

    # Fetch messages via GET request
    res = client.get('/api/messages', query_string={'with': 2})
    assert res.status_code == 200  # Expect success

    # Verify message exists in the response data
    data = res.get_json()
    assert 'messages' in data['data']
    assert any("Hello from unit test" in m['content'] for m in data['data']['messages'])

