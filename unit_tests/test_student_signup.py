import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from apps.front import create_app, db
from apps.front.models import FrontUser

@pytest.fixture
def test_app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(test_app):
    return test_app.test_client()

def test_signup_success(client):
    response = client.post('/signup/', data={
        'email': 'alice@example.com',
        'username': 'Alice',
        'stu_id': '11112222',
        'password1': 'Secret123',
        'password2': 'Secret123'
    })

    assert response.status_code == 200
    user = FrontUser.query.filter_by(email='alice@example.com').first()
    assert user is not None
    assert user.username == 'Alice'
