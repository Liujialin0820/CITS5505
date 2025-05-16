import pytest
from app import create_app
from exts import db
from config import Config
from apps.front.models import FrontUser

@pytest.fixture
def client():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'WTF_CSRF_ENABLED': False
    })

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_student_login(client):
    with client.application.app_context():
        user = FrontUser(username='Alice', email='alice@example.com', stu_id='11112222')
        user.password = 'Secret123'
        db.session.add(user)
        db.session.commit()

    response = client.post('/signin/', data={
        'email': 'alice@example.com',
        'password': 'Secret123'
    }, follow_redirects=True)

    # ✅ Check JSON response
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['code'] == 200
